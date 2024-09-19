def kb_to_prompt(system_prompt, kb):

    if type(kb[0]) == list:

        output_prompts = []

        for kb_i in kb:
            prompt = f"{system_prompt}\n\n--Knowledge Base:--\n"
            for instance in kb_i:
                prompt += "- {"
                for slot_name in instance:
                    if slot_name not in ["id", "introduction", "type", "location"]:
                        prompt += f'"{slot_name}": "{instance[slot_name]}", '
                prompt = prompt[:-2]
                prompt += "}\n"
            output_prompts.append(prompt)

        return output_prompts

    elif type(kb[0]) == dict:
        prompt = f"{system_prompt}\n\nKnowledge Base:\n"
        for instance in kb:
            prompt += "- {"
            for slot_name in instance:
                if slot_name not in ["id", "introduction", "type", "location"]:
                    prompt += f'"{slot_name}": "{instance[slot_name]}", '
            prompt = prompt[:-2]
            prompt += "}\n"
        return prompt

def instructions_to_prompt(user_prompt, user_instructions):

    if type(user_instructions) in [list, dict]:
        output_prompts = []
        for instruction_i in user_instructions:
            if type(user_instructions) == list:
                instruction_i_text = instruction_i
            else:
                instruction_i_text = user_instructions[instruction_i]
            prompt = f"{user_prompt}\n\nInstruction:\n{instruction_i_text}"
            output_prompts.append(prompt)
        return output_prompts
    elif type(user_instructions) == str:
        return f"{user_prompt}\n\nInstruction:\n{user_instructions}"
    else:
        print("ERROR: user_instruction has unexpected type.")