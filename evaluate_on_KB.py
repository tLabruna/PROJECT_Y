from chat_prompting import ChatGenerator
from templates import TEMPLATES, USER_INSTRUCTIONS
from retriever_pipeline import build_slot_extraction_prompt_eval, build_intent_extraction_prompt_eval, parse_rest_available_string
import json
from word2number import w2n
from utils import load_json, parse_input_string

VERBOSE = False

KB_path = "restaurant_db"
kb = load_json(f"KB/{KB_path}.json")

def check_alignment(name, food, price, area, choice, no_rest, kb):
    # Normalize the inputs for comparison
    name = name.lower() if name else None
    food = food.lower() if food else None
    price = price.lower() if price else None
    area = area.lower() if area else None
    choice = choice if choice else 0
    try: choice = int(choice)
    except: 
        try: choice = w2n.word_to_num(choice)
        except: pass

    # Function to check if a restaurant matches the given criteria
    def matches_criteria(restaurant):
        if name and name not in restaurant['name'].lower() and restaurant['name'].lower() not in name:
            return False
        if food and restaurant['food'].lower() != food:
            return False
        if price and restaurant['pricerange'].lower() != price:
            return False
        if area and restaurant['area'].lower() != area:
            return False
        return True

    # Check for alignment with the KB
    matches = [restaurant for restaurant in kb if matches_criteria(restaurant)]

    # print(f"Matches: {matches}")

    # Handling the `name` condition
    if name:
        if no_rest:
            return len(matches) == 0
        return len(matches) > 0

    # Handling the conditions when `name` is not defined
    if any([food, price, area]):
        if no_rest:
            return len(matches) == 0
        if type(choice) == int:
            return len(matches) == choice if choice >= 2 else len(matches) > 0
        return len(matches) > 0


    # Default return if no criteria are defined
    return False

llama_gen = ChatGenerator()
llama_gen.restaurants = kb

tot_system_turns = 0
tot_alignment = 0

errors = {}

for i in range(131):
    # if i < 4: continue
    # if i != 4: break
    errors[i] = []
    
    try:
        print(f"Tot KB-alignment: {tot_alignment}/{tot_system_turns} ({round(100*tot_alignment/tot_system_turns,2)}%)")
    except: pass
    print(i)

    log_path = f"logs/log_diag-{i}_retrieve_mwoz_rag_x10"
    try: log = load_json(f"{log_path}.json")
    except: continue
    for turn in log:
        if turn["role"] != "system": continue
        system_message = turn["text"]

        # print(system_message)

        # Extract slots

        prompt = build_slot_extraction_prompt_eval(system_message)
        query_values_str = llama_gen.prompt_model(prompt,single_prompt=True, temperature=0)
        parsed_query_values_list = parse_input_string(query_values_str, "system")
        if not parsed_query_values_list: continue

        # print(parsed_query_values_list)

        # Extract intent

        prompt = build_intent_extraction_prompt_eval(system_message)
        rest_available_str = llama_gen.prompt_model(prompt,single_prompt=True, temperature=0)

        parsed_rest_available = parse_rest_available_string(rest_available_str)
        no_rest = not parsed_rest_available

        # print(f"No rest: {no_rest}")

        if VERBOSE:
            print(query_values_str)
            print(parsed_query_values_list)
            print(rest_available_str)
            print(parsed_rest_available)

        # Check KB alignment for each parsed query dictionary in the list

        KB_alignment = True 
        valid_turn = False

        for parsed_query_values in parsed_query_values_list:  # parsed_query_values_list is a list of dictionaries
            name = parsed_query_values["name"]
            food = parsed_query_values["food"]
            area = parsed_query_values["area"]
            price = parsed_query_values["pricerange"]
            choice = parsed_query_values["choice"]

            # Continue only if at least one criterion is provided
            if any([name, food, area, price]):
                valid_turn = True            

                # Check alignment for the current set of query values
                KB_alignment_i = check_alignment(
                    name=name, 
                    food=food, 
                    area=area, 
                    price=price, 
                    choice=choice, 
                    no_rest=no_rest, 
                    kb=kb
                )        


                if no_rest and KB_alignment_i:
                    KB_alignment = True
                    break

                if not KB_alignment_i:
                    KB_alignment = False
                    if not no_rest:
                        errors[i].append(system_message)
                        break
            else:
                continue        

        if valid_turn:
            tot_system_turns += 1

            # print(f"KB alignment: {KB_alignment}")

            if VERBOSE:
                print(f"KB alignment: {KB_alignment}")
            
            if no_rest and not KB_alignment:
                errors[i].append(system_message)

            if KB_alignment: tot_alignment +=1

print(f"Tot KB-alignment: {tot_alignment}/{tot_system_turns} ({round(100*tot_alignment/tot_system_turns,2)}%)")
# exit()
with open(f"KB-alignment_errors_rag_x10.json", "w") as f:
    json.dump(errors, f, indent=4)
