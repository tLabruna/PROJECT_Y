import json, re

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

import re
import json

def parse_input_string(input_str, role):
    # Use a regex to extract all JSON parts, allowing for newlines and spaces
    json_matches = re.findall(r'\{[\s\S]*?\}', input_str)
    
    if not json_matches:
        return None  # If no valid JSON objects are found, return None
    
    parsed_list = []
    
    for json_str in json_matches:
        try:
            # Parse each extracted JSON string into a dictionary
            parsed_dict = json.loads(json_str)
        except json.JSONDecodeError:
            continue  # Skip this JSON object if it is malformed
        
        # Ensure all necessary keys are present, fill with empty strings if missing
        if role == "system":
            expected_keys = ["name", "food", "area", "price", "address", "postcode", "phone", "choice"]
        else:
            expected_keys = ["name", "food", "area", "price"]

        for key in expected_keys:
            if key not in parsed_dict:
                parsed_dict[key] = ""
        
        # Optional: Renaming "price" to "pricerange" if needed
        if "price" in parsed_dict:
            parsed_dict["pricerange"] = parsed_dict.pop("price")
        
        # Add the parsed dictionary to the list
        parsed_list.append(parsed_dict)
    
    return parsed_list

def parse_input_string_function(input_str, role):
    # Use a regex to extract the <function=...>{...}</function> structure
    function_pattern = r'<function=[a-zA-Z_]+>(\{[\s\S]*?\})<\/function>'
    function_match = re.search(function_pattern, input_str)

    # If the structure is not found, return False
    if not function_match:
        function_pattern = r'<function=[a-zA-Z_]+>(\{[\s\S]*?\})$'
        function_match = re.search(function_pattern, input_str)
        if not function_match:
            return False

    # Extract the JSON part from the function structure
    json_str = function_match.group(1)

    try:
        # Parse the extracted JSON string into a dictionary
        parsed_dict = json.loads(json_str)
    except json.JSONDecodeError:
        return None  # If JSON is malformed, return None
    
    # Ensure all necessary keys are present, fill with empty strings if missing
    if role == "system":
        expected_keys = ["name", "food", "area", "pricerange", "address", "postcode", "phone", "choice"]
    else:
        expected_keys = ["name", "food", "area", "pricerange"]

    for key in expected_keys:
        if key not in parsed_dict:
            parsed_dict[key] = ""

    # Optional: Renaming "price" to "pricerange" if needed
    if "price" in parsed_dict:
        parsed_dict["pricerange"] = parsed_dict.pop("price")

    return parsed_dict