TEMPLATES = {
    "multiwoz": "You are the Cambridge TownInfo Centre, a system designed to help users maximize their experience in the city of Cambridge. Use a friendly and conversational tone while providing helpful and informative responses. All the information you provide must strictly rely on the Knowledge Base that you have been provided with. Ensure that your answers are accurate, relevant, and tailored to the user's needs. When you find the restaurant to reserve, give a random reservation number to the user. Be short and concise.",
    "multiwoz-retrieve": "You are the Cambridge TownInfo Centre, a system designed to help users maximize their experience in the city of Cambridge. Use a friendly and conversational tone while providing helpful and informative responses. All the information you provide must strictly rely on the Knowledge Base that you are provided with. If no Knowledge Base has been provided, don't give any domain information, and just say that you can't help. Ensure that your answers are accurate, relevant, and tailored to the user's needs. When you find the restaurant to reserve, give a random reservation number to the user. Be short and concise.",
    "multiwoz-retrieve-all": "You are the Cambridge TownInfo Centre, a system designed to help users maximize their experience in the city of Cambridge. Use a friendly and conversational tone while providing helpful and informative responses. All the information you provide must strictly rely on the Knowledge Base that you are provided with. Ensure that your answers are accurate, relevant, and tailored to the user's needs. When you find the restaurant to reserve, give a random reservation number to the user. Be short and concise.",
    "multiwoz-ita": "Sei l'assistente Cambridge InfoCittà, un sistema progettato per aiutare gli utenti a trarre il meglio dalla loro esperienza nella città di Cambridge. Usa un tono amichevole e conversazionale, fornendo risposte informative e utili. Tutte le informazioni che fornisci devono basarsi strettamente sulla Knowledge Base che ti è stata data. Assicurati che le tue risposte siano accurate, pertinenti, e mirate ai bisogni dell'utente. Sii breve.",
    "user": "You are a turist in the city of Cambridge and you are looking for a restaurant to dine in. Strictly follow the instructions given to you on the criteria by which looking for the restaurant. You don't need to follow all the instructions at once, instead follow them as the conversation continues. Be very brief, and go straight to the point. At the end, thank the system and say goodbye. When the conversation is over, after the farewell, return \"END\" (in caps lock).",
    "user-ita": "Sei un turista nella città di Cambridge e stai cercando un ristorante dove cenare. Basati strettamente sulle istruzioni che ti vengono fornite riguardo i criteri in base ai quali cercare il ristorante. Non seguire tutte le istruzioni subito, invece seguile passo passo durante la conversazione. Sii molto breve e vai subito al punto.",
    "bear_0": "",
    "bear_1": "Chat with me as a friend of mine."
    }

LLAMA_INSTRUCTIONS = {
    "function_calling": """You have access to the following function:

Use the function 'query_restaurant_kb' to 'Retrieve restaurant details based on specified name, food type, area, or price range':
{
  name: "query_restaurant_kb",
  description: "Retrieve restaurant details based on specified name, food type, area, or price range",
  parameters: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "The name of the restaurant (if provided)",
      },
      food: {
        type: "string",
        description: "Type of food (e.g., italian, mexican, chinese, etc.)",
      },
      area: {
        type: "string",
        description: "Location area (e.g., north, south, east, west, or centre)",
      },
      pricerange: {
        type: "string",
        description: "Price range of the restaurant (e.g., cheap, moderate, expensive)",
      },
    },
    required: [],
  },
}

If you choose to call a function ONLY reply in the following format with no prefix or suffix:

<function=example_function_name>{"example_name": "example_value"}</function>
""",
"function_calling_mapping": """You have access to the following function:

Use the function 'query_restaurant_kb' to 'Retrieve restaurant details based on specified name, food type, area, or price range':
{
  name: "query_restaurant_kb",
  description: "Retrieve restaurant details based on specified name, food type, area, or price range",
  parameters: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "The name of the restaurant (if provided)",
      },
      food: {
        type: "string",
        description: "Type of food (e.g., italian, mexican, chinese, etc.)",
      },
      area: {
        type: "string",
        description: "Location area (e.g., north, south, east, west, or centre)",
      },
      pricerange: {
        type: "string",
        description: "Price range of the restaurant (e.g., cheap, moderate, expensive)",
      },
    },
    required: [],
  },
}

Map the values from the message for 'food', 'area', and 'price' fields to the following options:

- Food types: italian, international, indian, chinese, modern european, european, british, gastropub, mexican, lebanese, vietnamese, spanish, french, japanese, portuguese, korean, turkish, asian oriental, african, mediterranean, seafood, thai, north american
- Areas: north, south, centre, east, west
- Price ranges: cheap, moderate, expensive

For example, if the message says "high price," map it to "expensive." If the term can be mapped to one of these values, use the corresponding option.

If you choose to call a function ONLY reply in the following format with no prefix or suffix:

<function=example_function_name>{"example_name": "example_value"}</function>

However, if the message does not require querying the restaurant knowledge base, simply provide the direct response to the user.

Reminder:
- If looking for real time information use relevant functions before falling back to brave_search
- Function calls MUST follow the specified format, start with <function= and end with </function>
- Required parameters MUST be specified
- Only call one function at a time
- Put the entire function call reply on one line
"""
}

USER_INSTRUCTIONS = {
    "diag_1": "Look for a restaurant called \"The Copper Kettle\". If that is not available, look for any restaurant serving British food; if there aren't any, look for any place in the North.",
    "diag_2": "Look for a restaurant called \"The Missing Sock\". If not available, look for a cheap place; if not available, look for international food.",
    "diag_3": "Look for a moderate priced restaurant. If not available, look for a cheap Italian place in the centre.",
    "diag_4": "Look for an Indian restaurant in the expensive range in the East. If not available, search for another area; if not available ask for any other type of food in the East.",
    "diag_5": "Look for cheap Greek food in the South. If not available, look for anything except Italian or Chinese."
}

GPT_INSTRUCTIONS = {
    "dialogue_eval": "You are a dialogue evaluator. Given a dialogue you have to return a list of symbols separated by commas, where each symbol is an evaluation of each turn in the dialogue. Only system turns must be considered.",
    
    "dialogue_eval_1turn": "You are a dialogue evaluator. Given a turn of a dialogue you have to return a number, which represents an evaluation of the turn in the dialogue. Return ONLY THE NUMBER, nothing else, no explanation.",
    
    "dialogue_eval_2turns": "You are a dialogue evaluator. Given a user turn and a system turn of a dialogue you have to return a number, which represents an evaluation of the system turn in the dialogue. Return ONLY THE NUMBER, nothing else, no explanation.",    

    "dialogue_eval_2turns_yn": "You are a dialogue evaluator. Given a user turn and a system turn of a dialogue you have to return a \"yes\" or \"no\", which represents an evaluation of the system turn in the dialogue. Don't provide any explanation.",    

    "KB_errors_1turn": "Given the following turn, previous conversational context and KB, return one of the following numbers: 1 - if the information of the message doesn't contradict the KB; 0 - if it contradicts the KB; 2 - if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if a message states a restaurant is 'south', but it's actually 'north' in the KB, return 0. If it says a restaurant serves 'Indian food' and also the KB states so, return 1",
    
    "KB_errors_old": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system's information doesn't contradict the KB; 0 - if it contradicts the KB; n - if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if the system states a restaurant is 'south', but it's actually 'north' in the KB, return 0. If it says a restaurant serves 'Indian food' and also the KB states so, return 1",
    "KB_errors": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't contradict the KB; 0 - if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells)",
    "out_of_KB": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't mention properties outside of the KB; 0 - if the system mentions something about the KB which is not explicited in the KB (e.g. says that the restaurant serves british and indian, but only indian is present in the KB); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells)",                 
    "KB_errors_gpt-tiz_2": "Given the following dialogue and knowledge base (KB), return a comma-separated sequence with these values: 1 if the system's information does not contradict the KB, 0 if it contradicts the KB, and n if it doesn't reference specific KB information. For example, if the KB states a restaurant is 'south' and the system says it is 'north', return 0. If the KB states a restaurant serves 'Indian food' and the system says it serves 'Indian food', return 1. If the system says 'Hello!', return n. The point is to annotate whether the system says things that are in conflict with the KB.",
    "out_of_KB_gpt-tiz_2": "Given the following dialogue and knowledge base (KB), return a comma-separated sequence with these values: 1 if the system does not add any information outside the KB, 0 if it mentions properties not present in the KB, and n if it doesn't reference specific KB information. For example, if the KB states a restaurant serves 'Indian food' and the system says it also serves 'pizza', return 0. If the KB states a restaurant is 'south' and the system says it's 'north', but does not mention anything outside the KB, return 1. If the system says 'Goodbye!', return n. The point is to annotate whether the model says things outside the scope of the KB.",
    "KB_errors_gpt-tiz": "Analyze the given dialogue and knowledge base (KB). For each system turn, return a comma-separated sequence with these values: 1 if the system's information does not contradict the KB, 0 if it contradicts the KB, and n if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if the KB states a restaurant is 'south' and the system says it is 'north', return 0. If the KB states a restaurant serves 'Indian food' and the system says it serves 'Indian food', return 1. If the system says 'Hello!', return n. The point is that I want to annotate whether the system says things that are in conflict with the content of the KB.",
    "out_of_KB_gpt-tiz": "Analyze the given dialogue and knowledge base (KB). For each system turn, return a comma-separated sequence with these values: 1 if the system does not add any information outside the KB, 0 if it mentions properties not present in the KB, and n if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if the KB states a restaurant serves 'Indian food' and the system says it also serves 'pizza', return 0. If the KB states a restaurant is 'south' and the system says it's 'north', but does not mention anything outside the KB, return 1. If the system says 'Goodbye!', return n. The point is that I want to annotate whether the model says things that go outside the scope of the KB.",
    "KB_errors_gpt": "Analyze the given dialogue and knowledge base (KB). For each system turn, return a comma-separated sequence with these values: 1 if the system's information does not contradict the KB, 0 if it contradicts the KB, and n if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if the system says a restaurant is 'north' but the KB says it's 'south', return 0. If the system says a restaurant serves 'Indian food' and the KB says the same, return 1. If the system greets the user with 'Hello!', return n.",
    "out_of_KB_gpt": "Analyze the given dialogue and knowledge base (KB). For each system turn, return a comma-separated sequence with these values: 1 if the system does not add any information outside the KB, 0 if it mentions properties not present in the KB, and n if it doesn't reference specific KB information (e.g., greetings or farewells). For example, if the KB states a restaurant serves 'Indian food' and the system says it also serves 'pizza', return 0. If the KB states a restaurant is 'north' and the system says it's 'south', but does not mention anything outside the KB, return 1. If the system says 'Goodbye!', return n.",
    "KB_errors_0": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't contradict the KB; 0 - if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells)",
    "out_of_KB_0": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't talk about properties of the KB which are not in the KB; 0 - if the system mentions something about the KB, which is not explicited in the KB (e.g. says that the restaurant serves british and indian, but only indian is present in the KB); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells)",
    "KB_errors_2": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't contradict the KB (e.g. says a restaurant is at north, and it's actually at north); 0 - if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells). As an example, the dialogue User: I want a restaurant at south, System: X is at south, User: is it expensive?, System: Yes KB: restaurant X (price:expensive, area:north) - must be annotated as 0,1",
    "out_of_KB_2": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if the system doesn't talk about properties of the KB which are not in the KB (e.g. mentiones only the price and the area, which are in the KB); 0 - if the system mentions something about the KB, which is not explicited in the KB (e.g. says that the restaurant serves british and indian, but only indian is present in the KB, or says that a restaurant has WiFi, and there is no mention of that in the KB); n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells). As an example, the dialogue User: I want a restaurant at south, System: X is at south, User: what food do they serve?, System: British but they also offer very good pizzas KB: restaurant X (food:british, area:north) - must be annotated as 1,0",
    "KB_eval": "Given the following dialogue and knowledge base (KB), return a sequence of values separated by commas, one for each system turn. The possible values are: 1 - if everything is correct with respect to the KB; 2 - if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south), but doesn't made up things that are not included in the KB; 3 - if the system mentions something about the KB which is not there (e.g. says that the restaurant serves british and indian, but only indian is present in the KB), but doesn't contradict the KB; 4 - if the system both contradicts the KB and made up things that are not included in the KB; n - if the system doesn't make any reference to specific information in the KB (e.g. greetings or farewells).",

    "n_detect_1": "Given the following user and system turns, return 1 if the system turn says something that must be checked over some external source to understand if the information provided is correct, 0 otherwise.",
    "n_detect": "Given the following user and system turns, return 1 if the system turn contains information that requires verification from an external source to ensure its accuracy, 0 otherwise.",
    "n_detect_2": "Given the following user and system turns, return 1 if the system turn makes reference to an external domain knowledge, 0 otherwise.",

    "KB_errors_2turns_0": "Given the following user turn, system turn, and Knowledge Base (KB), return 1 if the system is consistent with what contained in the KB, 0 otherwise (e.g. says that a restaurant is at north, but it's actually at south).",
    "KB_errors_2turns_best": "Given the following user turn, system turn, and Knowledge Base (KB), return 0 if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south), 1 otherwise.",
    "out_of_KB_2turns_0": "Given the following user turn, system turn, and Knowledge Base (KB), return 1 if the system doesn't mention properties outside of the KB; 0 otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",
    "out_of_KB_2turns_best": "Given the following user turn, system turn, and Knowledge Base, return 1 if the system doesn't mention properties outside of the Knowledge Base, 0 otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",
    "out_of_KB_2turns_2": "Given the following user turn, system turn, and Knowledge Base, return 1 if the system turn only mentions properties found within the Knowledge Base, 0 otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",

    "KB_errors_2turns_yn_0": "I need your assistance in evaluating a conversation between a user and a chatbot powered by a large language model (LLM). In this interaction, the user is seeking information about restaurants. I will provide a user's query, the LLM's response, and a knowledge base (KB) containing information about restaurants that the LLM can use to provide the most accurate response. Please determine if the LLM has responded accurately and in alignment with the KB data. Answer \"yes\" if it has, and \"no\" if the LLM has incorrectly used the KB.",
    "out_of_KB_2turns_yn_0": "I need your assistance in evaluating a conversation between a user and a chatbot powered by a large language model (LLM). In this interaction, the user is seeking information about restaurants. I will provide a user's query, the LLM's response, and a knowledge base (KB) containing information about restaurants that the LLM can use to provide the most accurate response. Please determine if the LLM has responded accurately and strictly used only the information provided in the KB. Answer \"yes\" if it has, and \"no\" if the LLM has added any new information not present in the KB.",

    "KB_errors_2turns_yn_1": "Given the following user turn, system turn, and Knowledge Base (KB), determine if the system has responded accurately and in alignment with the KB. Return \"no\" if the system contradicts the KB (e.g. says that a restaurant is at north, but it's actually at south), \"yes\" otherwise.",
    "out_of_KB_2turns_yn_1": "Given the following user turn, system turn, and Knowledge Base, determine if the system has responded using only the properties in the KB. Return \"yes\" if the system doesn't mention properties outside of the Knowledge Base, \"no\" otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",

    "KB_errors_2turns_yn_2": "Given the following user turn, system turn, and Knowledge Base (KB), the system was consistent with the KB? Answer \"yes\" if the response was correct with respect to the KB, \"no\" otherwise.",
    "out_of_KB_2turns_yn_2": "Given the following user turn, system turn, and Knowledge Base (KB), the system responded using only the properties in the KB? Answer \"yes\" if the system doesn't mention properties outside the KB, \"no\" otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",

    "KB_errors_2turns_yn": "Given the following user turn, system turn, and Knowledge Base (KB), the system was consistent with the KB? Answer \"yes\" if the response was correct with respect to the KB, \"no\" otherwise (e.g. says that a restaurant is at north, but it's actually at south).",
    "out_of_KB_2turns_yn_3": "Given the following user turn, system turn, and Knowledge Base (KB), the system sticks to the properties of the KB? Answer \"yes\" if the system doesn't mention properties outside the KB, \"no\" otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB).",

    # "out_of_KB_2turns_yn": "Given the following user turn, system turn, and Knowledge Base (KB), the system was adherent to the properties within the KB? Answer \"yes\" if the system only mentions properties found in the KB, \"no\" otherwise (e.g., if the system states that a restaurant serves both British and Indian cuisine, but the KB only lists Indian cuisine)."        
    "out_of_KB_2turns_yn": "Given the following user turn, system turn, and Knowledge Base, return \"yes\" if the system doesn't mention properties outside of the Knowledge Base, \"no\" otherwise (e.g. says that the restaurant serves british and indian, but only indian is present in the KB)."
}

