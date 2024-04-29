from math import e
from Model import *
import json
from argparse import ArgumentParser
import os
import yaml
import sys

parser = ArgumentParser() 

parser.add_argument("-p",dest="profile_num", type = str, help="Set User profile", default="0")

parser.add_argument("-pt",dest="prompt_type", type = str, help="Select one prompt type from 1) General Questions 2) MCQ", default="general_questions")

parser.add_argument("-m",dest="model_name", type = str, help="Model selection", default="gpt4")

parser.add_argument("-lv",dest="lv", type = str, help="Provide TELer Prompt Level. Select from lv0, lv1, lv2, lv3, lv4", default="4")

parser.add_argument("-pl",dest="profile_location", type = str, help="Profile Location : [USA, India, Bangladesh]", default="USA")

parser.add_argument("-cuda",dest="cuda", type = str, help="Cuda device number", default="1")




# get system content
with open("./config/system_prompt.yaml", "r") as f:
    system_content = yaml.safe_load(f)

# get user profile
# with open("./config/user_profile.json", "r") as f:
#     user_profile = json.load(f)
with open("./config/evaluation-profile.json", "r") as f:
    user_profile = json.load(f)
    
    
# get prompts
with open("./config/prompts.json", "r") as f:
    prompts = json.load(f)

args = parser.parse_args()
profile = user_profile[f"{args.profile_location}_user_profiles"][f"profile_{args.profile_num}"]

if args.lv in ["lv0", "lv1"]:
    system_content= system_content["target_system_content"][f"lv{args.lv}"]
else:
    system_content= system_content["target_system_content"][f"lv{args.lv}"].format(profile=json.dumps(profile))

history = [{"user_profile":profile,"role": "system", "content": system_content}]
# print("History: ", history)


# model = gpt.GPT3Model(sysetm_role=system_content)

if args.model_name in ["GPT3","gpt3"]:  
    model = gpt.GPTModel(system_role=system_content)
elif args.model_name in ["GPT4","gpt4"]:
    model = gpt.GPTModel(system_role=system_content)
elif args.model_name in ["claude","Claude"]:
    model = claude.ClaudeModel(system_role=system_content)
elif args.model_name in ["gemini","Gemini"]:
    model = gemini.GeminiModel(system_role=system_content)
elif args.model_name in ["Llama3","LLaMA3","llama3"]:
    pass
elif args.model_name in ["Mistral","mistral"]:
    pass
elif args.model_name in [f"Phi3-min","phi3-min","phi"]:
    model = phi.phi3mini(system_role=system_content,cuda_device=args.cuda)


# TODO: select category from profile desc
# while True:
    # prompt = "What is the purpose of life?"
    
all_categoiries = list(profile.keys())
conversation_history = {}
for category_key in all_categoiries:
    cat_prompts = list(prompts["category"][category_key][args.prompt_type].values())
    conversation_history[category_key] = []
    for prompt in cat_prompts:
        if prompts in ["exit", "quit", "bye"]:
            break 
        print("\nUSER: ", prompt)
        try:
            conversation = model.generate_response(prompt)
        
        except:
            conversation = "Error"
        
        conversation_history[category_key].append({"user":prompt,"assistant": conversation})
        print("\nAssistant: ", conversation)
        print(f"\n###################################### ---- profile_{args.profile_num}\n")
history.append(conversation_history)
    

# save
save_path = f"./results/user_profile_{args.profile_location}/{args.model_name}"
if not os.path.exists(save_path):
    os.makedirs(save_path)

count = len(os.listdir(save_path)) + 1
with open(f"{save_path}/profile_{args.profile_num}_{args.prompt_type}.json", "a") as f:
    json.dump(history, f, indent=4)
