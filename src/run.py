from math import e
from turtle import color

from click import progressbar
from Model import *
import json
from argparse import ArgumentParser
import os
import yaml
import sys
from tqdm import tqdm
from Model.vllm.vllm_session import VllmSession
import time

parser = ArgumentParser() 

parser.add_argument("-p",dest="profile_num", type = str, help="Set User profile", default="4")

parser.add_argument("-pt",dest="prompt_type", type = str, help="Select one prompt type from 1) General Questions 2) MCQ", default="general_questions")

parser.add_argument("-m",dest="model_name", type = str, help="Model selection", default="Llama3")

parser.add_argument("-lv",dest="lv", type = str, help="Provide TELer Prompt Level. Select from lv0, lv1, lv2, lv3, lv4", default="5")

parser.add_argument("-pl",dest="profile_location", type = str, help="Profile Location : [USA, India, Bangladesh]", default="Bangladesh")

parser.add_argument("-cuda",dest="cuda", type = str, help="Cuda device number", default="1")
parser.add_argument("-save",dest="save", type = bool, help="save data", default=True)

# get system content
with open("./config/system_prompt.yaml", "r") as f:
    system_content = yaml.safe_load(f)

# get user profile
# with open("./config/user_profile.json", "r") as f:
#     user_profile = json.load(f)

with open("./config/evaluation-profile.json", "r") as f:
    user_profile = json.load(f)
    
with open("./src/Model/vllm/vllm_config.yaml","r") as f:
    vllm_config = yaml.safe_load(f)
    
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


if args.model_name in ["GPT3","gpt3"]:  
    model = gpt.GPTModel(system_role=system_content)
elif args.model_name in ["GPT4","gpt4"]:
    model = gpt.GPTModel(system_role=system_content)
elif args.model_name in ["claude","Claude","claude3"]:
    model = claude.ClaudeModel(system_role=system_content)
elif args.model_name in ["gemini","Gemini"]:
    model = gemini.GeminiModel(system_role=system_content)
elif args.model_name in ["Llama3","LLaMA3","llama3"]:
    model = VllmSession(vllm_config,"meta-llama/Meta-Llama-3-8B-Instruct", system_message=system_content,temperature = 1.0)
elif args.model_name in ["Mistral","mistral"]:
    model = VllmSession(vllm_config,"mistralai/Mistral-7B-Instruct-v0.1",system_message=system_content,temperature = 1.0)
elif args.model_name in [f"Phi3-min","phi3-min","phi"]:
    model = phi.phi3mini(system_role=system_content,cuda_device=args.cuda)

filtered_list= dict(
pronouns_ = [1,2,7,8,9],
political_views_ = [2,4,5,7,9],
religious_veiws_ = [1,3,5,6,7],
geolocation_ = [1,2,4,7,10],
education_level_ = [1,5,6,7,10],
tech_background_ = [2,3,4,5,7],
mental_health_ = [1,2,3,4,6],
accessibility_ = [1,2,3,7,13],
age_group_ = [1,2,4,5,9],
financial_status_ = [3,6,7,10,12]
)




# This code can be used when we want one prompt passed at a time.     
all_categoiries = list(profile.keys())
conversation_history = {}
retires = 3
delay = 5
for cat_idx, category_key in enumerate(all_categoiries):
    if category_key == "tech background":
        category_key_ = "tech_background_"
    else:
        category_key_ = category_key + "_"
    # cat_prompts = list(prompts["category"][category_key][args.prompt_type].values()) # to get all prompts
    cat_prompts = [list(prompts["category"][category_key][args.prompt_type].values())[i-1] for i in filtered_list[category_key_]] # to get filtered_prompts
    
    conversation_history[category_key] =[]
    
    progress_bar = tqdm(total=len(cat_prompts))

    for idx,prompt in enumerate(cat_prompts):
        # print(f"\n ###############  profile_{args.profile_num} --- {category_key} --- questions # {idx} ###############\n")
        progress_bar.set_description(f"profile_{args.profile_num} --- {category_key}")
        
        if prompt in ["exit", "quit", "bye"]:
            conversation_history[category_key].append({"user":prompt,"assistant": "exited"})
            progress_bar.update(1)
            # print(f"user:{prompt},assistant: exited")
            break 
        print("\nUSER: ", prompt)
        # handling exceptions errors:
        for _ in range(retires):
            try:
                conversation = model.generate_response(prompt)
                break
            except Exception as e:
                # conversation = "Error"
                print("There is an error profile_{args.profile_num} --- {category_key} --- question {idx}")
                time.sleep(delay)
                delay = delay * 2
            except KeyboardInterrupt:
                sys.exit()
        conversation_history[category_key].append({"user":prompt,"assistant": conversation})
        print("\nAssistant: ", conversation)
        progress_bar.update(1)

history.append(conversation_history)
progress_bar.close()


# passing all prompts as a list. 
# all_categoiries = list(profile.keys())
# conversation_history = {}
# for cat_idx, category_key in enumerate(all_categoiries):
#     cat_prompts = list(prompts["category"][category_key][args.prompt_type].values())
#     conversation_history[category_key] = []
#     # for idx,prompt in enumerate(cat_prompts):
#     print(f"\n ###############  profile_{args.profile_num} --- {category_key} --- questions ###############\n")
#     try:
#         conversation = model.generate_response(cat_prompts)
#     except:
#         conversation = "Error"
#     profile_conv = []
#     for k,v in zip(cat_prompts,conversation):
#         profile_conv.append({"user":k,"assistant":v})
#     conversation_history[category_key].append(profile_conv)
#     # print(profile_conv)
#     # breakpoint()
# history.append(conversation_history)

# print(history)

# save
if args.save == True:
    save_path = f"./results/user_profile_{args.profile_location}/{args.model_name}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    count = len(os.listdir(save_path)) + 1
    with open(f"{save_path}/profile_{args.profile_num}_{args.prompt_type}.json", "a") as f:
        json.dump(history, f, indent=4)
        
    print(f"saving at: {save_path}/profile_{args.profile_num}_{args.prompt_type}.json")
    

