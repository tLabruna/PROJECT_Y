from chat_prompting import ChatGenerator
from templates import TEMPLATES
import random
from utils import load_kb

SAVE_FILE = False

system_prompt = TEMPLATES["multiwoz"]

llama_gen = ChatGenerator(model="llama")

llama_gen.restaurants = load_kb('KB/restaurant_db.json')

llama_gen.add_system_prompt(system_prompt)
log = llama_gen.start_live_mode(retrieve=True)

if SAVE_FILE:
    file_name = f"log_setting_retrieve_{str(random.randint(1,1000))}.json"

    print(f"File named {file_name} correctely saved.")

