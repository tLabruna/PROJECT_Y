import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from llama import Dialog, Llama
import torch, openai, json, re
import torch.nn as nn
from retriever_query import find_restaurants
from utils import load_json, parse_input_string
from retriever_pipeline import build_slot_extraction_prompt, build_system_prompt, parse_query_values, retrieve_restaurants
from build_prompt import kb_to_prompt

# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

class ChatGenerator:
    """
    This class facilitates prompting on the Llama-3 models, providing both inline
    and data loading modalities.
    """
    
    def __init__(self, model="llama", dep_id="", ckpt_dir="/data01/PROJECT_X/llama3/Meta-Llama-3.1-8B-Instruct", tokenizer_path="/data01/PROJECT_X/llama3/Meta-Llama-3.1-8B-Instruct/tokenizer.model", max_seq_len=8192, max_batch_size=6):
        """
        When initialized, the object creates an empty list of dialogues
        and sets the Llama generator.
        """
        self.model = model
        self.dialogues = []
        self.max_seq_len = max_seq_len

        if model == "llama":
            print("Initializing Llama")  
            self.generator = self.build_generator_llama(ckpt_dir, tokenizer_path, max_seq_len, max_batch_size)
            # self.generator = nn.DataParallel(self.generator)  # Avvolgi il generatore con nn.DataParallel
            # self.generator = self.generator.cuda()          
            # self.generator = self.build_generator_llama(ckpt_dir, tokenizer_path, max_seq_len, max_batch_size)
            print("Llama initialized successfully")
        
        elif model == "gpt":
            print("Initializing GPT")
            if dep_id:
                self.generator = self.build_generator_gpt(dep_id)
            else:
                self.generator = self.build_generator_gpt()
            print("GPT initialized successfully")
            
    
    def build_generator_llama(self, ckpt_dir, tokenizer_path, max_seq_len, max_batch_size):
        print(f"Building generator with ckpt_dir={ckpt_dir}, tokenizer_path={tokenizer_path}, max_seq_len={max_seq_len}, max_batch_size={max_batch_size}")
        return Llama.build(
            ckpt_dir=ckpt_dir,
            tokenizer_path=tokenizer_path,
            max_seq_len=max_seq_len,
            max_batch_size=max_batch_size,
        )

    def build_generator_gpt(self, dep_id="gpt-4o"):        
        self.deployment_id = dep_id
        return openai.AzureOpenAI(
            api_key="ca72e43668824cd090e6ea210fe3cd3b",  
            api_version="2024-02-01",
            azure_endpoint = "https://hlt-nlp.openai.azure.com/"
        )
    
    def prompt_model(self, message="", i=-1, max_gen_len=None, temperature=0.6, top_p=0.9, single_prompt=False, additional_system_prompt=""):
        """
        This method prompts the Llama model. The single prompt method means
        that we are not keeping track of the conversation. Otherwise, we store
        the past conversation in the dialogues variable and we use it for prompting
        the model.
        """        
        if single_prompt: 
            if not message:
                raise Exception("Empty prompt message")
            prompt = [{"role": "user", "content": message}]

        else:
            if message:
                self.add_to_context(message, "user", i) 
            if additional_system_prompt:
                self.add_system_prompt(additional_system_prompt, i, first_turn=False)           
            prompt = self.dialogues[i]
        
        if self.model == "llama":
            old_len = 0
            c = 0
            while 1:
                if c >= 10:
                    print("Error: Can't reduce prompt length")
                    break
                # print("Trying prompt length...")
                prompt_tokens = self.generator.formatter.encode_dialog_prompt(prompt)
                # prompt_tokens = self.generator.module.formatter.encode_dialog_prompt(prompt)
                if len(prompt_tokens) == old_len:
                    Exception("Prompt length problem.")
                old_len = len(prompt_tokens)
                if len(prompt_tokens) > self.max_seq_len:
                    c += 1
                    is_dialog_full = self.remove_from_context(i)
                    if not is_dialog_full:
                        raise Exception("Prompt message is too long.")
                else:
                    break
        

        if self.model == "llama":
            result = self.generator.chat_completion(
                [prompt],
                max_gen_len=max_gen_len,
                temperature=temperature,
                top_p=top_p
            )
            # result = self.generator.module.chat_completion(
            #     [prompt],
            #     max_gen_len=max_gen_len,
            #     temperature=temperature,
            #     top_p=top_p,
            # )

            system_output = result[0]['generation']['content']
        
        elif self.model == "gpt":            
            with torch.no_grad():  
                response = self.generator.chat.completions.create(
                    model=self.deployment_id,
                    messages=prompt,
                    temperature=temperature,
                )
                system_output = response.choices[0].message.content.strip()

        if not single_prompt:
            self.add_to_context(system_output, "assistant", i)
        
        return system_output

    def add_to_context(self, message, role, i=-1):
        """
        This method adds user/system messages to the context, which is stored in the
        dialogues variable.
        """
        message_formatted = {"role": role, "content": message}
        for i in range(i + 1 - len(self.dialogues)):
            self.dialogues.append([])
        if self.dialogues:
            self.dialogues[i].append(message_formatted)
        else:
            self.dialogues = [[message_formatted]]

    def remove_from_context(self, i):
        if self.dialogues[i][0]["role"] == "system":
            self.dialogues[i] = [self.dialogues[i][0]] + self.dialogues[i][2:]
        else:
            self.dialogues[i] = self.dialogues[i][1:]   
        return len(self.dialogues[i])
    
    def add_system_prompt(self, message, i=-1, first_turn=True):
        """
        This method add a system prompt, by default as the first turn in a dialogue.
        """
        message_formatted = {"role": "system", "content": message}
        if i >= len(self.dialogues):
            for _ in range(i + 1 - len(self.dialogues)):
                self.dialogues.append([])
        if self.dialogues:
            if self.dialogues[i]:
                if first_turn:
                    if self.dialogues[i][0]["role"] == "system":
                        self.dialogues[i][0] = message_formatted
                    else:
                        self.dialogues[i] = [message_formatted] + self.dialogues[i]
                else:
                    self.dialogues[i].append(message_formatted)
            else:
                self.dialogues[i] = [message_formatted]
        else:
            self.dialogues = [[message_formatted]]
    
    def retrieve_from_user_message(self, user_message, i=-1):
        # Build prompt including user input
        prompt = build_slot_extraction_prompt(user_message)
        # print(prompt)

        # Prompt model to get the slot values
        query_values_str = self.prompt_model(prompt,single_prompt=True)
        print(query_values_str)

        # Parse the slot values in a structured form                
        parsed_query_values_list = parse_input_string(query_values_str, "user")
        print(parsed_query_values_list)

        output = ""

        for parsed_query_values in parsed_query_values_list:

            if "name" in parsed_query_values and "area" in parsed_query_values and "food" in parsed_query_values and "pricerange" in parsed_query_values and (parsed_query_values["name"] or parsed_query_values["area"] or parsed_query_values["food"] or parsed_query_values["pricerange"]):
                # Get retrieved restaurants
                retrieved_restaurants = self.query_restaurant_kb(name=parsed_query_values["name"], area=parsed_query_values["area"], food=parsed_query_values["food"], pricerange=parsed_query_values["pricerange"])

                if len(retrieved_restaurants) == 0:
                    output = "No restaurant have been found based on user criterias. Don't provide information on any restaurant and inform the user that they should revise their criteria."
                elif len(retrieved_restaurants) >= 10:
                    output = "Too many restaurants have been found. Don't provide information on any restaurant and inform the user that they should add more criteria, so you can refine your search."
                else:
                    # Build final prompt
                    return kb_to_prompt("Your answer should strictly rely to the following Knowledge Base.", retrieved_restaurants)
        return output
    
    def start_live_mode(self, retrieve=False):
        """
        This method allows to start a live in-line modality with the model.
        """
        log = []
        i = 0
        while 1:
            user_message = input("User: ")
            print()
            if user_message == "exit": break
            log.append({"turn": i, "role": "user", "text": user_message})
            i += 1

            if retrieve:
                self.retrieve_from_user_message(user_message)

            system_message = self.prompt_model(user_message)

            print(f"System: {system_message}")
            log.append({"turn": i, "role": "system", "text": system_message})
            i += 1
            print()
        return log
    
    def start_llama_to_llama_mode(self, user_i, system_i, turns=8, escape_token="", retrieve=False, verbose=False):
        """
        This method allows two llamas to talk to each other, until the number of turns is reached.
        """
        log = []
        i = 0
        system_message = ""
        while i < turns:
            user_message = self.prompt_model(system_message, user_i)
            if escape_token and escape_token in user_message: break
            log.append({"turn": i, "role": "user", "text": user_message})
            i += 1
            additional_system_prompt = ""
            if retrieve:
                additional_system_prompt = self.retrieve_from_user_message(user_message, system_i)
            if verbose:
                print(self.dialogues)
                print("--------------")
            system_message = self.prompt_model(user_message, system_i, additional_system_prompt = additional_system_prompt)
            if escape_token and escape_token in user_message: break
            log.append({"turn": i, "role": "system", "text": system_message})
            # self.add_to_context(system_message, "user", user_i)
            i += 1
        return log
    
    def query_restaurant_kb(self, name="", area="", food="", pricerange=""):
        results = []
        
        # Exact match (case insensitive)
        for restaurant in self.restaurants:
            if (name.lower() == restaurant["name"].lower() or not name) and \
            (area.lower() == restaurant["area"].lower() or not area) and \
            (food.lower() == restaurant["food"].lower() or not food) and \
            (pricerange.lower() == restaurant["pricerange"].lower() or not pricerange):
                results.append(restaurant)
        
        # If exact matches found, return them
        if results:
            return results

        # Relaxed match (substring check)
        for restaurant in self.restaurants:
            if (name.lower() in restaurant["name"].lower() or not name) and \
            (area.lower() in restaurant["area"].lower() or not area) and \
            (food.lower() in restaurant["food"].lower() or not food) and \
            (pricerange.lower() in restaurant["pricerange"].lower() or not pricerange):
                results.append(restaurant)
        
        # If substring matches found, return them
        if results:
            return results        

        # Loosest match (one is contained in the other)
        for restaurant in self.restaurants:
            if (self._contains_either_way(name, restaurant["name"]) or not name) and \
            (self._contains_either_way(area, restaurant["area"]) or not area) and \
            (self._contains_either_way(food, restaurant["food"]) or not food) and \
            (self._contains_either_way(pricerange, restaurant["pricerange"]) or not pricerange):
                results.append(restaurant)
        
        return results

    def _contains_either_way(self, query_term, db_term):
        # Check if one term is contained in the other (case insensitive)
        query_term = query_term.lower()
        db_term = db_term.lower()
        return query_term in db_term or db_term in query_term


    
    def reset_dialogues(self):
        """
        This method deletes the whole conversation history.
        """
        self.dialogues = []

if __name__ == "__main__":
    llama_gen = ChatGenerator(model="llama")
    llama_gen.start_live_mode(retrieve=True)
    exit()

    input_user = "I am looking for a French restaurant ."
    prompt = f"""
Extract the values for name, food, area, and price from the following sentence and return them in the format: "name:'x', food:'y', area:'z', price:'j'". If any of these values are not mentioned, leave them empty. Ensure the values are reported exactly as mentioned in the sentence.

- name: The name of the restaurant or establishment.
- food: The type of food or dish mentioned.
- area: The location or neighborhood where the restaurant is situated.
- price: The cost of the food or meal, including currency if mentioned.

Sentence: {input_user}

Output:"""
    
#     prompt = f"""
# Given the following message, extract and return the restaurant details in the format name:'x', food:'y', area:'z', price:'j'. If any detail is not mentioned in the message, leave the corresponding string empty.

# Output Format:
# name:'x', food:'y', area:'z', price:'j'

# Example:
# If the message is "I'm looking for a Mexican restaurant called El Patio in the downtown area with an affordable price," the output should be:
# name:'El Patio', food:'Mexican', area:'downtown', price:'affordable'

# Message:
# {input_user}

# Extracted Details:
# """
    
    query_values_str = llama_gen.prompt_model(prompt,single_prompt=True)
    print(query_values_str)
    kb_file_path = 'KB/restaurant_db.json'
    restaurants = load_json(kb_file_path)
    llama_gen.restaurants = restaurants
    parsed_query_values = parse_input_string(query_values_str, "system")
    print(parsed_query_values)
    if "name" in parsed_query_values and "area" in parsed_query_values and "food" in parsed_query_values and "pricerange" in parsed_query_values:
        filtered_restaurants = llama_gen.query_restaurant_kb(name=parsed_query_values["name"], area=parsed_query_values["area"], food=parsed_query_values["food"], pricerange=parsed_query_values["pricerange"])
    else:
        print("Error while parsing extracting query values")
    print(filtered_restaurants)
    exit()
    
    # while 1:
    #     input_user = input("User: ")
    #     prompt = f"Extract from the following message the values for Name, Food, Area and Price and return the output in the form name:'x', food:'y', area:'z', price:'j'. Don't add anything else. If some of the values are not in the message, leave the correspondent string empty.\n\nMessage:\n{input_user}"
    #     query_values_str = llama_gen.prompt_model(prompt,single_prompt=True)
    #     prompt = 

    exit()
    llama_gen.add_system_prompt("Rispondi come fossi Vasco Rossi")
    print(llama_gen.prompt_model("Come stai?"))
    # llama_gen.start_live_mode()

    