from Model import gpt
import json
from argparse import ArgumentParser
import os
import yaml
import sys

parser = ArgumentParser() 

parser.add_argument("-p","--profile_num", type = str, dest="Mention profile that you want to set. Like Profile_1", help="Set User profile", default="profile_0")

parser.add_argument("-pt","--prompt_type", type = str, dest="Select one prompt type from 1) General Questions 2) MCQ", help="Select Prompt type", default="general_questions")

# TODO: Set argument to select model


# get system content
with open("./config/system_prompt.yaml", "r") as f:
    system_content = yaml.safe_load(f)

# get user profile
with open("./config/user_profile.json", "r") as f:
    user_profile = json.load(f)
    
# get prompts
with open("./config/prompts.json", "r") as f:
    prompts = json.load(f)


profile = user_profile["user_profile"]["profile_0"]
system_content= system_content["target_system_content"]["lv4"].format(profile=json.dumps(profile))

history = [{"user_profile":profile,"role": "system", "content": system_content}]
print("History: ", history)


model = gpt.GPT3Model(sysetm_role=system_content)
args = parser.parse_args()


# TODO: select category from profile desc
while True:
    # prompt = "What is the purpose of life?"
    cat_prompts = list(prompts["category"]["pronouns"]["general_questions"].values())
    for prompt in cat_prompts:
        if prompts in ["exit", "quit", "bye"]:
            break  
        print("\nUSER: ", prompt)
        conversation = model.generate_response(prompt)
        history.append({"user":prompt,"assistant": conversation})
        print("\nAssistant: ", conversation)
        print("\n######################################\n")
    break

# save
