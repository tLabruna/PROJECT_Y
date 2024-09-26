from chat_prompting import ChatGenerator
from templates import TEMPLATES, USER_INSTRUCTIONS
from retriever_pipeline import build_slot_extraction_prompt_eval, build_intent_extraction_prompt_eval, parse_rest_available_string
import json
from word2number import w2n
from utils import load_json, parse_input_string

VERBOSE = False

KB_path = "restaurant_db"
kb = load_json(f"KB/{KB_path}.json")

data_path = "MWOZ_restaurant/val_dials"
data = load_json(f"{data_path}.json")

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

def is_no_offer(d_act):
    return "Restaurant-NoOffer" in d_act

def map_to_da_slot(slot):
    slot = slot.lower()
    map = [["postcode", "post"], ["address", "addr"], ["pricerange", "price"]]
    for m in map:
        if slot == m[0]:
            return m[1]
    return slot

def count_slots(d_act):
    c = 0
    for domain_intent in d_act:
        for da in d_act[domain_intent]:
            da_slot_name = da[0].lower()
            da_slot_value = da[1].lower()
            if da_slot_name != "none" and da_slot_value not in ["none", "?"]:
                c += 1
    return c

def slot_present(slot_name, slot_value, d_act):
    slot_name = map_to_da_slot(slot_name)
    for domain_intent in d_act:
        for da in d_act[domain_intent]:
            da_slot_name = da[0].lower()
            da_slot_value = da[1].lower()
            if slot_name == da_slot_name:
                if slot_value.lower() == da_slot_value or \
                    (slot_name == "name" and (slot_value.lower() in da_slot_value or \
                                              da_slot_value in slot_value.lower())):
                    return True
    return False


llama_gen = ChatGenerator()
llama_gen.restaurants = kb

# tot_kb_system_turns = 0
# tot_correct_intent = 0

tot_correct_slots = 0
tot_annotated_slots = 0
tot_slots = 0

i = 0

f = open("log_slot_prompt_4.txt", "a")

for d in data:
    i += 1
    print(f"{i}/{len(data)}")
    for l in data[d]["log"]:
        turn_id = l["turn_id"]
        if turn_id % 2 == 0: continue

        system_message = l["text"]

        # Extract slots

        prompt = build_slot_extraction_prompt_eval(system_message)
        query_values_str = llama_gen.prompt_model(prompt,single_prompt=True)
        parsed_query_values_list = parse_input_string(query_values_str, "system")
        if not parsed_query_values_list: continue

        # Extract intent

        # prompt = build_intent_extraction_prompt_eval(system_message)
        # rest_available_str = llama_gen.prompt_model(prompt,single_prompt=True)

        # parsed_rest_available = parse_rest_available_string(rest_available_str)
        # no_rest = not parsed_rest_available

        if VERBOSE:
            print(query_values_str)
            print(parsed_query_values_list)
            # print(rest_available_str)
            # print(parsed_rest_available)

        # Check KB alignment for each parsed query dictionary in the list

        # correct_intent = True
         
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
                
                for slot_name in parsed_query_values:
                    slot_value = parsed_query_values[slot_name]
                    if slot_value == "": continue
                    if slot_present(slot_name, slot_value, l["dialog_act"]):
                        tot_correct_slots += 1
                    else:
                        print("--")
                        print(system_message)
                        print(f"{slot_name}, {slot_value}")
                        f.write(system_message + "\n")
                        f.write(f"{slot_name}, {slot_value}\n")
                    tot_annotated_slots += 1

                # Check alignment for the current set of query values
                # KB_alignment_i = check_alignment(
                #     name=name, 
                #     food=food, 
                #     area=area, 
                #     price=price, 
                #     choice=choice, 
                #     no_rest=no_rest, 
                #     kb=kb
                # )

                # if not KB_alignment_i:
                #     KB_alignment = False
                #     break
            else:
                continue

        if valid_turn:
            # tot_kb_system_turns += 1

            tot_slots += count_slots(l["dialog_act"])

            # if VERBOSE:
            #     print(f"KB alignment: {KB_alignment}")

            # if KB_alignment: tot_alignment +=1

            # if is_no_offer(l["dialog_act"]) == no_rest:
            #     tot_correct_intent += 1    
            # else:
            #     print("Error")
            #     print(system_message)
            #     print(rest_available_str)
            #     f.write(system_message + "\n")
            #     f.write(rest_available_str + "\n")

    # print(f"Tot correct intents: {tot_correct_intent}/{tot_kb_system_turns} ({round(100*tot_correct_intent/tot_kb_system_turns,2)}%)")

    # Calcolo delle metriche
    precision = tot_correct_slots / tot_annotated_slots if tot_annotated_slots > 0 else 0
    recall = tot_correct_slots / tot_slots if tot_slots > 0 else 0
    precision = tot_correct_slots / tot_annotated_slots if tot_annotated_slots > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Stampa dei risultati
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")
    print(f"Slot Totali (Gold): {tot_slots}")
    print(f"Slot Annotati (Predetti): {tot_annotated_slots}")
    print(f"Slot Corretti: {tot_correct_slots}")

# print(f"Tot correct intents: {tot_correct_intent}/{tot_kb_system_turns} ({round(100*tot_correct_intent/tot_kb_system_turns,2)}%)")
f.close()
