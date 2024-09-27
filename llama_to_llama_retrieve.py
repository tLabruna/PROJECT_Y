from chat_prompting import ChatGenerator
from templates import TEMPLATES, USER_INSTRUCTIONS
from build_prompt import kb_to_prompt, instructions_to_prompt
import json, os
from utils import load_json

USE_ALL_KB = True
USE_MWOZ_INSTRUCTIONS = True
VERBOSE = False

user_prompt = TEMPLATES["user"]

KB_path = "restaurant_db_x2"

kb = load_json(f"KB/{KB_path}.json")
val_dials = load_json("MWOZ_restaurant/val_dials.json")

system_prompt = TEMPLATES["multiwoz-retrieve"]

if USE_ALL_KB:
    system_prompt = kb_to_prompt(TEMPLATES["multiwoz-retrieve-all"], kb)

RETRIEVE = True
if USE_ALL_KB:
    RETRIEVE = False

llama_gen = ChatGenerator()
llama_gen.restaurants = kb

if USE_MWOZ_INSTRUCTIONS:
    user_instructions = message_dict = {key: value['goal']['message'] for key, value in val_dials.items()}
    user_prompts = instructions_to_prompt(user_prompt, user_instructions)
else:
    user_prompts = instructions_to_prompt(user_prompt, USER_INSTRUCTIONS)

all_dialogues = {}
all_logs = {}

for i in range(len(user_prompts)):
    # if i == 50: break
    # log_path = f"log_diag-{i}_retrieve_mwoz_new"
    # try: load_json(f"{log_path}.json")
    # except: continue
    user_prompt_i = user_prompts[i-1]
    # try:
    print(f"Dialogue #{i} starting...\n")
    
    llama_gen.add_system_prompt(user_prompt_i, 0)
    llama_gen.add_to_context("Hi, I'm here to help you find a restaurant.", "user", 0)
    llama_gen.add_system_prompt(system_prompt, 1)
    log = llama_gen.start_llama_to_llama_mode(0,1,7, retrieve=RETRIEVE, verbose=VERBOSE)

    all_dialogues[i] = llama_gen.dialogues
    all_logs[i] = log

    # except:
        # llama_gen.reset_dialogues()
        # continue
    llama_gen.reset_dialogues()

with open(f"logs/log-all_x2.json", "w") as f:
    json.dump(all_dialogues, f, indent=4)

file_name = "logs/log_diag-all_x2.json"

with open(file_name, "w") as f:
    json.dump(log, f, indent=4)

print(f"File named {file_name} correctely saved.")
print("------------------------------")

    # exit()
