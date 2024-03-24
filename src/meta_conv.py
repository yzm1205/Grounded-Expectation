from gpt_prompt import ChatGPT_conversation
import os
import json

with open("./src/config.json", "r") as f:
    config = json.load(f)

system_context = config['system_content']['2']
print(f"system: {system_context} \n")

history = [{"role": "system", "content": system_context}]

while True:
    prompt = input('\n User: ')
    if prompt in ["exit", "quit", "bye"]:
        break   
    # history.append({'role': 'user', 'content': prompt})
    conversation = ChatGPT_conversation(prompt,history)
    print("\nassistant: ", conversation)
    
    
count = len(os.listdir("./history_records")) + 1
with open(f"./history_records/conv_{count}.json", "w") as f:
    json.dump(history, f, indent=4)