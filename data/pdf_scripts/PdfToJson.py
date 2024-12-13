import pdfplumber
import json

def pdf_to_json(pdf_path, json_path):
    # Initialize an empty list to store all school data
    schools = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Split text into lines
                lines = text.split("\n")
                school = {}
                i = 0
                
                while i < len(lines):
                    line = lines[i].strip()
                    
                    if line.startswith("Name:"):
                        school["Name"] = line.split(":", 1)[1].strip()
                    elif line.startswith("Possible Other Name(s):"):
                        school["Possible Other Name(s)"] = line.split(":", 1)[1].strip()
                    elif line.startswith("School Address"):
                        school["School Address"] = line.split("Address", 1)[1].strip()
                    elif line.startswith("Start Date:"):
                        school["Start Date"] = line.split(":", 1)[1].strip()
                    elif line.startswith("End Date:"):
                        school["End Date"] = line.split(":", 1)[1].strip()
                    elif "Housing" in line:
                        school["Housing"] = "Yes" if "Yes" in line else "No"
                    elif "Education" in line:
                        school["Education"] = "Yes" if "Yes" in line else "No"
                    elif "Federal Support" in line:
                        school["Federal Support"] = "Yes" if "Yes" in line else "No"
                    elif "Timeframe" in line:
                        school["Timeframe"] = "Yes" if "Yes" in line else "No"
                    elif line.startswith("School Type"):
                        school_type = line.split("Type", 1)[1].strip()
                        school["School Type"] = school_type
                    elif line.startswith("General Notes"):
                        general_notes = line.split("Notes", 1)[1].strip()
                        i += 1
                        while i < len(lines) and lines[i].strip() and not lines[i].startswith("Name:"):
                            general_notes += f" {lines[i].strip()}"
                            i += 1
                        school["General Notes"] = general_notes
                        continue  # Skip increment to properly handle the next line

                    i += 1
                
                if school:  # Add school data if the dictionary is not empty
                    schools.append(school)

    # Write the final data to JSON
    with open(json_path, "w") as json_file:
        json.dump(schools, json_file, indent=4)

# Define file paths
pdf_path = "new_output.pdf"  # Replace with your PDF file path
json_path = "school.json"    # Replace with your desired JSON output file path

# Run the function
pdf_to_json(pdf_path, json_path)
print(f"Data extracted and saved to {json_path}")
