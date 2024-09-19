import json

MAX_LEN = False

with open("KB/restaurant_db.json", "r") as f:
    kb = json.load(f)

USER_INSTRUCTIONS = {
    "diag_1": "Look for a restaurant called \"The Copper Kettle\". If that is not available, look for any restaurant serving British food; if there aren't any, look for any place in the North.",
    "diag_2": "Look for a restaurant called \"The Missing Sock\". If not available, look for a cheap place; if not available, look for international food.",
    "diag_3": "Look for a moderate priced restaurant. If not available, look for a cheap Italian place in the centre.",
    "diag_4": "Look for an Indian restaurant in the expensive range in the East. If not available, search for another area; if not available ask for any other type of food in the East.",
    "diag_5": "Look for cheap Greek food in the South. If not available, look for anything except Italian or Chinese."
}

all_slots = {"name":[], "area": [], "food":[], "pricerange":[]}

for instance in kb:
    if instance["name"] not in all_slots["name"]:
        all_slots["name"].append(instance["name"])
    if instance["area"] not in all_slots["area"]:
        all_slots["area"].append(instance["area"])
    if instance["food"] not in all_slots["food"]:
        all_slots["food"].append(instance["food"])
    if instance["pricerange"] not in all_slots["pricerange"]:
        all_slots["pricerange"].append(instance["pricerange"])                

auto_prompts = {"diag_1": [], "diag_2": [], "diag_3": [], "diag_4": [], "diag_5": []}

# diag_1
prompt_0 = "Look for a restaurant called \""
for name in all_slots["name"]:
    if MAX_LEN and len(auto_prompts["diag_1"]) == MAX_LEN:
        break
    prompt_1 = f"{prompt_0}{name}\" . If that is not available, look for any restaurant serving "
    for food in all_slots["food"]:
        if MAX_LEN and len(auto_prompts["diag_1"]) == MAX_LEN:
            break
        prompt_2 = f"{prompt_1}{food} food; if there aren't any, look for any place in the "            
        for area in all_slots["area"]:
            prompt_3 = f"{prompt_2}{area}."
            auto_prompts["diag_1"].append(prompt_3)
            if MAX_LEN and len(auto_prompts["diag_1"]) == MAX_LEN:
                print("Max len reached.")
                break

# diag_2
prompt_0 = "Look for a restaurant called \""
for name in all_slots["name"]:
    if MAX_LEN and len(auto_prompts["diag_2"]) == MAX_LEN:
        break
    prompt_1 = f"{prompt_0}{name}\". If not available, look for a "
    for pricerange in all_slots["pricerange"]:
        if MAX_LEN and len(auto_prompts["diag_2"]) == MAX_LEN:
            break
        prompt_2 = f"{prompt_1}{pricerange} place; if not available, look for "            
        for food in all_slots["food"]:
            prompt_3 = f"{prompt_2}{food} food."
            auto_prompts["diag_2"].append(prompt_3)
            if MAX_LEN and len(auto_prompts["diag_2"]) == MAX_LEN:
                print("Max len reached.")
                break

# diag_3
prompt_0 = "Look for a "
for pricerange in all_slots["pricerange"]:
    if MAX_LEN and len(auto_prompts["diag_3"]) == MAX_LEN:
        break
    prompt_1 = f"{prompt_0}{pricerange} priced restaurant. If not available, look for a "
    for pricerange_2 in all_slots["pricerange"]:
        if MAX_LEN and len(auto_prompts["diag_3"]) == MAX_LEN:
            break
        if pricerange_2 == pricerange: continue
        prompt_2 = f"{prompt_1}{pricerange_2} "            
        for food in all_slots["food"]:
            if MAX_LEN and len(auto_prompts["diag_3"]) == MAX_LEN:
                break
            prompt_3 = f"{prompt_2}{food} place in the "
            for area in all_slots["area"]:
                prompt_4 = f"{prompt_3}{area}."
                auto_prompts["diag_3"].append(prompt_4)
                if MAX_LEN and len(auto_prompts["diag_3"]) == MAX_LEN:
                    print("Max len reached.")
                    break

# diag_4
prompt_0 = "Look for an "
for food in all_slots["food"]:
    if MAX_LEN and len(auto_prompts["diag_4"]) == MAX_LEN:
        break
    prompt_1 = f"{prompt_0}{food} restaurant in the "
    for pricerange in all_slots["pricerange"]:
        if MAX_LEN and len(auto_prompts["diag_4"]) == MAX_LEN:
            break
        prompt_2 = f"{prompt_1}{pricerange} range in the "            
        for area in all_slots["area"]:
            prompt_3 = f"{prompt_2}{area}. If not available, search for another area; if not available ask for any other type of food in the {area}."
            auto_prompts["diag_4"].append(prompt_3)
            if MAX_LEN and len(auto_prompts["diag_4"]) == MAX_LEN:
                print("Max len reached.")
                break

# diag_5
prompt_0 = "Look for "
for pricerange in all_slots["pricerange"]:
    if MAX_LEN and len(auto_prompts["diag_5"]) == MAX_LEN:
        break
    prompt_1 = f"{prompt_0}{pricerange} "
    for food in all_slots["food"]:
        if MAX_LEN and len(auto_prompts["diag_5"]) == MAX_LEN:
            break
        prompt_2 = f"{prompt_1}{food} food in the "            
        for area in all_slots["area"]:
            if MAX_LEN and len(auto_prompts["diag_5"]) == MAX_LEN:
                break
            prompt_3 = f"{prompt_2}{area}. If not available, look for anything except "
            for food_2 in all_slots["food"]:
                if MAX_LEN and len(auto_prompts["diag_5"]) == MAX_LEN:
                    break
                if food_2 == food: continue
                prompt_4 = f"{prompt_3}{food_2} or "
                for food_3 in all_slots["food"]:
                    if food_3 in [food, food_2]: continue
                    prompt_5 = f"{prompt_4}{food_3}."
                    auto_prompts["diag_5"].append(prompt_5)
                    if MAX_LEN and len(auto_prompts["diag_5"]) == MAX_LEN:
                        print("Max len reached.")
                        break

with open("templates_auto.json", "w") as f:
    json.dump(auto_prompts, f, indent=4)
