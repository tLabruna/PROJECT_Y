# from chat_prompting import ChatGenerator
from utils import load_json, parse_input_string
from templates import TEMPLATES

def build_slot_extraction_prompt():
    return f"""You have access to the following function:

Use the function 'query_restaurant_kb' to 'Retrieve restaurant details based on specified name, food type, area, or price range':
{{
  name: "query_restaurant_kb",
  description: "Retrieve restaurant details based on specified name, food type, area, or price range",
  parameters: {{
    type: "object",
    properties: {{
      name: {{
        type: "string",
        description: "The name of the restaurant (if provided)",
      }},
      food: {{
        type: "string",
        description: "Type of food (e.g., italian, mexican, chinese, etc.)",
      }},
      area: {{
        type: "string",
        description: "Location area (e.g., north, south, east, west, or centre)",
      }},
      pricerange: {{
        type: "string",
        description: "Price range of the restaurant (e.g., cheap, moderate, expensive)",
      }},
    }},
    required: [],
  }},
}}

Map the values from the message for 'food', 'area', and 'price' fields to the following options:

- Food types: italian, international, indian, chinese, modern european, european, british, gastropub, mexican, lebanese, vietnamese, spanish, french, japanese, portuguese, korean, turkish, asian oriental, african, mediterranean, seafood, thai, north american
- Areas: north, south, centre, east, west
- Price ranges: cheap, moderate, expensive

For example, if the message says "high price," map it to "expensive." If the term can be mapped to one of these values, use the corresponding option.

If the message explicitly requires querying the restaurant details (e.g., mentioning restaurant names or attributes such as food type or price), call the function in the following format:

<function=query_restaurant_kb>{{name": "x", "food": "y", "area": "z", "pricerange": "j"}}</function>

However, if the message does not require querying the restaurant knowledge base, simply provide the direct response to the user.
"""

def build_slot_extraction_prompt_eval(input_system):
    return f"""Given the following message, extract and return the restaurant details in the format:

[
    {{
        "name": "",
        "food": "",
        "area": "",
        "price": "",        
        "address": "",
        "phone": "",
        "postcode": "",
        "choice": ""
    }},
    ...
]

If the message contains information for more than one restaurant or multiple values for the same slot (e.g., multiple types of food, multiple areas, etc.), return each set of details as a separate dictionary inside the list. For example, if multiple types of food are mentioned, each food type should appear in its own dictionary entry, even if the other information remains the same.

**Only extract values that are explicitly mentioned in the message. Do not infer or assume any values. If a specific slot is not mentioned, leave it as an empty string.**

Try to map the values for 'food', 'area', and 'price' fields to one of the following options, but only if they are explicitly mentioned:

food:
italian, international, indian, chinese, modern european, european, british, gastropub, mexican, lebanese, vietnamese, spanish, french, japanese, portuguese, korean, turkish, asian oriental, african, mediterranean, seafood, thai, north american

area:
north, south, centre, east, west

price:
cheap, expensive, moderate

If the message contains a term that can be mapped to one of these values, use the corresponding option. For example, if the message says "high price", map it to "expensive". 

Name is the name of the restaurant. 
Address is the address of the restaurant.
Phone is the phone number of the restaurant.
Postcode is the postcode of the restaurant.
Choice is the number of restaurants that the system says it found, but leave it as an empty string for individual restaurants unless a specific number is mentioned in the message.

Example:
If the message is "On the south end, in the expensive price range, we have Mexican, Italian, Indian, and Chinese foods to choose from", the output should be:
[
    {{
        "name": "",
        "food": "mexican",
        "area": "south",
        "price": "expensive",
        "address": "",
        "phone": "",
        "postcode": "",
        "choice": ""
    }},
    {{
        "name": "",
        "food": "italian",
        "area": "south",
        "price": "expensive",
        "address": "",
        "phone": "",
        "postcode": "",
        "choice": ""
    }},
    {{
        "name": "",
        "food": "indian",
        "area": "south",
        "price": "expensive",
        "address": "",
        "phone": "",
        "postcode": "",
        "choice": ""
    }},
    {{
        "name": "",
        "food": "chinese",
        "area": "south",
        "price": "expensive",
        "address": "",
        "phone": "",
        "postcode": "",
        "choice": ""
    }}
]

Return only the JSON, nothing else.

Message: "{input_system}"

Extracted Details as JSON: """

def build_intent_extraction_prompt_eval(input_system):
    return f"""Given a message from a system designed to help users find restaurants, determine if the system is stating that there are no restaurants meeting the user criteria.

Instructions:

- If the message clearly indicates that there are no restaurants available that meet the user’s criteria (e.g., "no restaurants found" or "no restaurants available"), return "NOREST".
- If the message refers to something unrelated to restaurant availability, such as a booking issue (e.g., "restaurant is fully booked" or "booking unsuccessful"), or contains general information about restaurants, return "ok".
- Return "NOREST" only if the system explicitly states that no restaurants meet the user’s search criteria. Return "ok" in all other cases.

Examples:

1. Message: "I found 3 such restaurants in the north."
   Output: "ok"

2. Message: "I'm sorry, but there are no restaurants offering Caribbean food."
   Output: "NOREST"

3. Message: "Here are a few restaurants in the city center."
   Output: "ok"

4. Message: "Booking was not successful, as the restaurant is fully booked."
   Output: "ok"

Return only "NOREST" or "ok", without adding any explanation.

Message: "{input_system}"

Output:"""

def parse_rest_available_string(rest_available_str):
    message = rest_available_str.lower() 
    if 'norest' in message:
        return False
    return True


def build_system_prompt(retrieved_restaurants):
    prompt = f"""{TEMPLATES['multiwoz']}\nKB:\n"""
    for rest in retrieved_restaurants:
        prompt += f"- Name: {rest['name']}, Area: {rest['area']}, Price: {rest['pricerange']}, Food: {rest['food']}, Address: {rest['address']}, Postcode: {rest['postcode']}, Phone: {rest['phone']}"
        if "introduction" in rest:
            prompt += f", Description: {rest['introduction']}"
        prompt += "\n"
    prompt = prompt[:-1]
    return prompt

def parse_query_values(query_values_str, llama_gen, kb_file_path='KB/restaurant_db.json'):
    restaurants = load_json(kb_file_path)
    llama_gen.restaurants = restaurants
    return parse_input_string(query_values_str)

def retrieve_restaurants(llama_gen, parsed_query_values):
    if "name" in parsed_query_values and "area" in parsed_query_values and "food" in parsed_query_values and "pricerange" in parsed_query_values:
        return llama_gen.query_restaurant_kb(name=parsed_query_values["name"], area=parsed_query_values["area"], food=parsed_query_values["food"], pricerange=parsed_query_values["pricerange"])
    print("Error while parsing extracting query values")


if __name__ == "__main__":
    # llama_gen = ChatGenerator(model="llama")
    # input_user = "I am looking for a French restaurant ."

    # # Build prompt including user input
    # prompt = build_slot_extraction_prompt(input_user)

    # # Prompt model to get the slot values
    # query_values_str = llama_gen.prompt_model(prompt,single_prompt=True)
    # print(query_values_str)

    # # Parse the slot values in a structured form
    # parsed_query_values = parse_query_values(query_values_str, llama_gen)
    # print(parsed_query_values)

    # # Get retrieved restaurants
    # retrieved_restaurants = retrieve_restaurants(parsed_query_values)
    # print(retrieved_restaurants)

    # # Build final prompt
    # prompt = build_system_prompt(llama_gen, retrieved_restaurants)
    # print(prompt)

    # # Get system answer
    # system_answer = llama_gen.prompt_model(prompt,single_prompt=True)
    # print(system_answer)
    pass