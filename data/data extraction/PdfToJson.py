import pdfplumber
import re
import json


def extract_school_data(pdf_path):
    """
    Extract data for each school from the PDF file.
    """
    schools_data = []

    # Patterns for extracting fields
    patterns = {
        "school_name": r"^\s*([A-Z][\w\s',-]+),\s*([A-Z][\w\s'-]+)\s*$",
        "dates_of_operation": r"Dates of Operation:\s*([\d–]+)",
        "current_diocese": r"Current Diocese:\s*([\w\s'-]+)",
        "previous_dioceses": r"Previous Diocese(?:s)? Involved:\s*((?:●.*\n)+)",
        "religious_orders": r"Religious Orders who worked at the Parish / School:\s*((?:●.*\n)+)",
        "on_reservation": r"On a Reservation:\s*(Yes|No)",
        "on_doi_list": r"On the Department of the Interior List:\s*(Yes|No)",
        "tribal_nations": r"Tribal Nations Impacted.*:\s*((?:●.*\n)+)",
        "notes": r"Notes:\s*(.*)"
    }

    def extract_multiline_list(text):
        """Extract list items starting with bullet points."""
        return [line.strip("●").strip() for line in text.split("\n") if line.strip()]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            school_data = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    if key in ["previous_dioceses", "religious_orders", "tribal_nations"]:
                        school_data[key] = extract_multiline_list(match.group(1))
                    else:
                        school_data[key] = match.group(1).strip()

            if "school_name" in school_data:
                schools_data.append(school_data)

    return schools_data


def save_to_json(data, output_path="schools_data.json"):
    """
    Save extracted data to a JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_path}")


# Main execution
pdf_path = "List-5.5.2023.pdf"  # Replace with the correct path
output_path = "extracted_schools_data.json"

# Extract and save the data
schools_data = extract_school_data(pdf_path)
save_to_json(schools_data, output_path)
