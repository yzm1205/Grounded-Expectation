import json
import os
import sys
import time
import yaml
from argparse import ArgumentParser
from tqdm import tqdm
from Model.vllm.vllm_session import VllmSession
from Model import gpt, claude, gemini, phi
from myutils.utils import mkdir_p,full_path
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Argument Parsing
def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-p", dest="profile_num", type=str, default="4", help="Set User profile")
    parser.add_argument("-pt", dest="prompt_type", type=str, default="general_questions", help="Select one prompt type")
    parser.add_argument("-m", dest="model_name", type=str, default="Llama3", help="Model selection")
    parser.add_argument("-lv", dest="lv", type=str, default="5", help="TELer Prompt Level. Select from lv0 to lv5")
    parser.add_argument("-pl", dest="profile_location", type=str, default="India", help="Profile Location")
    parser.add_argument("-cuda", dest="cuda", type=str, default="1", help="Cuda device number")
    parser.add_argument("-save", dest="save", type=bool, default=False, help="Save data")
    return parser.parse_args()

# Load Configuration Files
def load_config_files():
    with open("./config/system_prompt.yaml", "r") as f:
        system_content = yaml.safe_load(f)
    
    with open("./config/evaluation-profile.json", "r") as f:
        user_profile = json.load(f)
    
    with open("./src/Model/vllm/vllm_config.yaml", "r") as f:
        vllm_config = yaml.safe_load(f)
    
    with open("./config/prompts.json", "r") as f:
        prompts = json.load(f)

    return system_content, user_profile, vllm_config, prompts

# Initialize the model based on user selection
def initialize_model(args, system_content, vllm_config):
    if args.model_name in ["GPT3", "gpt3", "GPT4", "gpt4"]:
        model = gpt.GPTModel(system_role=system_content,model_name="gpt-3.5-turbo-0125")
    elif args.model_name in ["claude", "Claude", "claude3"]:
        model = claude.ClaudeModel(system_role=system_content,model_name="claude-3-sonnet-20240229")
    elif args.model_name in ["gemini", "Gemini"]:
        model = gemini.GeminiModel(system_role=system_content,model_name="gemini-1.5-flash")
    elif args.model_name in ["Llama3", "LLaMA3", "llama3"]:
        model = VllmSession(vllm_config, "meta-llama/Meta-Llama-3-8B-Instruct", system_message=system_content, temperature=1.0)
    elif args.model_name in ["Mistral", "mistral"]:
        model = VllmSession(vllm_config, "mistralai/Mistral-7B-Instruct-v0.1", system_message=system_content, temperature=1.0)
    elif args.model_name in ["Phi3-min", "phi3-min", "phi"]:
        model = phi.phi3mini(system_role=system_content, cuda_device=args.cuda)
    return model

# Prepare conversation history with system and user profiles
def prepare_conversation_history(profile, system_content, lv):
    if lv in ["lv0", "lv1"]:
        system_message = system_content["target_system_content"][f"lv{lv}"]
    else:
        system_message = system_content["target_system_content"][f"lv{lv}"].format(profile=json.dumps(profile))
    
    history = [{"user_profile": profile, "role": "system", "content": system_message}]
    return history, system_message

# Manage conversation flow
def handle_conversations(args, prompts, profile, model,history):
    filtered_list = get_filtered_list()
    all_categories = list(profile.keys())
    if sys.gettrace():
        all_categories = all_categories[:2]
    conversation_history = {}
    conversation_history.update(history[-1])
    
    retries = 3
    delay = 5

    for category_key in all_categories:
        category_key_ = transform_category_key(category_key)
        cat_prompts = [list(prompts["category"][category_key][args.prompt_type].values())[i-1] for i in filtered_list[category_key_]]
        if sys.gettrace():
            cat_prompts = cat_prompts[:2]
        conversation_history[category_key] = []
        
        progress_bar = tqdm(total=len(cat_prompts), desc=f"profile_{args.profile_num} --- {category_key}")
        
        for idx, prompt in enumerate(cat_prompts):
            if prompt in ["exit", "quit", "bye"]:
                conversation_history[category_key].append({"user": prompt, "assistant": "exited"})
                progress_bar.update(1)
                break
            
            conversation = retry_conversation(model, prompt, retries, delay)
            conversation_history[category_key].append({"user": prompt, "assistant": conversation})
            # history.append(conversation_history)
            # history[-1]["Prompting"][category_key] = conversation_history
            save_conversation_history(args, conversation_history)  # Save after each prompt
            progress_bar.update(1)

        progress_bar.close()
    return conversation_history

# Retry the conversation in case of errors
def retry_conversation(model, prompt, retries, delay):
    redo_prompt = ""
    for _ in range(retries):
        try:
            # if model.model == "claude-3-sonnet-20240229":
            #     return model.generate_response(redo_prompt + prompt )
            # else:
                # return model.generate_response(redo_prompt + prompt + "\n Make sure the reponses are short and relevant withing 25-30 word limit. No Preamble")
            return model.generate_response(redo_prompt + prompt )
        except Exception as e:
            print(f"There was an error: {str(e)}")
            redo_prompt = "There was an error. Please try again. Here is the prompt: "
            time.sleep(delay)
            delay *= 2
            
        except KeyboardInterrupt:
            sys.exit()

# Transform category key names
def transform_category_key(category_key):
    return "tech_background_" if category_key == "tech background" else category_key + "_"

# Example filter list (you might want to pass this dynamically)
def get_filtered_list():
    return {
        "pronouns_": [1, 2, 7, 8, 9],
        "political_views_": [2, 4, 5, 7, 9],
        "religious_veiws_": [1, 3, 5, 6, 7],
        "geolocation_": [1, 2, 4, 7, 10],
        "education_level_": [1, 5, 6, 7, 10],
        "tech_background_": [2, 3, 4, 5, 7],
        "mental_health_": [1, 2, 3, 4, 6],
        "accessibility_": [1, 2, 3, 7, 13],
        "age_group_": [1, 2, 4, 5, 9],
        "financial_status_": [3, 6, 7, 10, 12]
    }

# Save conversation history
def save_conversation_history(args, history):
    if args.save:
        save_path = mkdir_p(f"./results_new/user_profile_{args.profile_location}/{args.model_name}")
        # if not os.path.exists(save_path):
        #     os.makedirs(save_path)
        
        with open(f"{save_path}/profile_{args.profile_num}_{args.prompt_type}.json", "w") as f:
            json.dump(history, f, indent=4)
        
        # print(f"Saved at: {save_path}/profile_{args.profile_num}_{args.prompt_type}.json")

# Main function
def main():
    args = parse_arguments()
    # After loading and initializing
    logger.info(f"Model: {args.model_name}")
    logger.info(f"Location: {args.profile_location}")
    logger.info(f"Profile Number: {args.profile_num}")
    
    # logger.info(f"System Content: {system_content[:30]}...")  # First 30 chars
    
    system_content, user_profile, vllm_config, prompts = load_config_files()
    profile = user_profile[f"{args.profile_location}_user_profiles"][f"profile_{args.profile_num}"]
    logger.info(f"Profile: {profile}")
    history, system_message = prepare_conversation_history(profile, system_content, args.lv)

    model = initialize_model(args, system_message, vllm_config)
    conversation_history = handle_conversations(args, prompts, profile, model,history)
    
    if args.save:
        save_path = mkdir_p(f"./results_new/user_profile_{args.profile_location}/{args.model_name}")
        print(f"Saved at: {save_path}/profile_{args.profile_num}_{args.prompt_type}.json")

        
    
    # history.append(conversation_history)
    # save_conversation_history(args, history)

if __name__ == "__main__":
    main()
    print("Done!")