import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode_address(address):
    """Fetch latitude and longitude for a given address."""
    geolocator = Nominatim(user_agent="school_geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            return {"latitude": None, "longitude": None}
    except GeocoderTimedOut:
        return {"latitude": None, "longitude": None}

def add_geocoding_to_json(input_json_path, output_json_path):
    """Add geocoding data to each entry in the JSON file."""
    # Load the JSON data
    with open(input_json_path, "r") as input_file:
        data = json.load(input_file)

    # Iterate over each school and add geocoding data
    for school in data:
        address = school.get("School Address", "")
        if address:
            print(f"Geocoding address: {address}")
            geocode_result = geocode_address(address)
            school.update(geocode_result)
        else:
            print("No address found for this entry.")

    # Save the updated data to a new JSON file
    with open(output_json_path, "w") as output_file:
        json.dump(data, output_file, indent=4)

    print(f"Geocoded data saved to {output_json_path}")

# Define input and output JSON file paths
input_json_path = "school.json"  # Replace with your input JSON file
output_json_path = "output_with_geocoding.json"   # Replace with your desired output JSON file

# Run the function
add_geocoding_to_json(input_json_path, output_json_path)
