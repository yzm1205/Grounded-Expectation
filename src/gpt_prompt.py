import os
import json
from openai import OpenAI
import yaml
from argparse import ArgumentParser
from dotenv import load_dotenv
load_dotenv(dotenv_path="./src/.env")


"""
TODO:
1. create some example of prompts with keywords and see if the response is relevant
2. check if dictionary is suitable or not. 
3. create a benchmark: 
    - create a list of prompts for each generic keyword and also with some combination of keywords
    - generate responses with default gpt3.5-turbo-0125 for baseline
    - generate responses by passing generic keyword gpt3.5-turbo-0125 for benchmark
4. Test with TELER taxonomy
5. Try different models 
    - open source
        - Mistral
        - Llama2
        - Falcon
        - PalM-2
        - Dolly2 (From Databricks)
        - FLAN-T5 (from google)
    - GPT4
    - GPT3.5-turbo-0125
    - Phi
    -
    -
6. set system content from meta conversation. 
7. Create a simple web interface to test the model (can we test on simpal)
9. Perform annotation on the generated responses
89. Do user study. 
    
Q: For each model, we will have baselines and expectation results.

"""


parser = ArgumentParser()
# parser.add_argument("-gs","--guided_sys", dest=" System type",  action="store_true")
# parser.add_argument("ds","--default_sys", dest=" System type",  action="store_true")

parser.add_argument("-p","--profile_num", type = str, dest="profile_num", help="User profile", default="profile_0")

parser.add_argument("-pt","--prompts_type", type = str, dest="prompts_type", help="Prompts type", default="general_questions")

# parser.add_argument()

# print("gpt3_key") 
client = OpenAI(api_key=os.getenv("gpt3_key"))
model_id = 'gpt-3.5-turbo-0125'
# model_id = 'gpt-4'
args = parser.parse_args()
print(f"{model_id} : Running...\n\n")




with open("./src/keywords.yaml", "r") as f:
    config = yaml.safe_load(f)
    # print("done")
    
with open("./src/profile.json", "r") as f:
    profiles = json.load(f)
    

    
with open("./src/prompts.json", "r") as f:
    prompts = json.load(f)
    
default,guided=False,True
prompts_type = "MCQ"
# profile_number = list(profiles["user_profile"].keys())[1]
profile = profiles["user_profile"][args.profile_num]
print("Profile: ", args.profile_num)

def generate_system_prompt(default=default, guided=guided):
    if default:
        system_context = config["target_system_context_without_kv"]["1"] 
    elif guided:
        # system_context = config["target_system_context_with_kv"]["5"] 
        # system_context = system_context.replace("{keyword}", keyword)
        # system_context = system_context.replace("{keyword_value}", keyword_value)
        # system_context = system_context.replace("{gk}", f"{generic_keywords}")
        
        system_context= f"""You are a chat bot assiting people with their queries. The responses should be genereated for the user profile as {profile}. Note that, the repsonses should align with the user profile. For instance, example 1: If the user profile has 'age' keyword and its value is 'age' and the people to address are 'kids', then the chatbot should reply in a way that is suitable for kids. -  Similarly, Example 2: if the user profile has'political view' category and if its value is 'left wing', then the responses to the quires should address leftist people only. - Example 3: In the user profile, there could be multiple keywords such as 'age', political_view' and many more and its value could be 'adult', leftist' respectively. The keywords and its values define the user profile. So, generate responses such that it only intereset to that user profile.
        """
    else:
        raise ValueError("Invalid system context")
    
    return system_context
    
system_context = generate_system_prompt(default=default, guided=guided)
history = [{"role": "system", "content": system_context}]


def ChatGPT_conversation(prompt,history=[]):
   
    if "{profile}" in prompt:
        prompt = prompt.replace("{profile}", f"{profile}")
        # + f"Explian to {keyword_value} {keyword} group people. 
    response = client.chat.completions.create(  
        model=model_id,
        messages=[{"role": "system", 
                    "content": system_context},
                    {"role":"user",
                    "content": prompt }],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    history.append({"user":prompt,"assistant": response.choices[0].message.content}) 
    return response.choices[0].message.content


print(f"system: {system_context} \n")
while True:
    if default:
        prompts = input('\n User: ')
        if prompts in ["exit", "quit", "bye"]:
                break   
            # history.append({'role': 'user', 'content': prompt})
        conversation = ChatGPT_conversation(prompts,history)
        # print("\nUSER: ", prompts)
        print("\nAssistant: ", conversation)
        print("\n######################################\n")
    if guided:
        cat_prompts = list(prompts["category"]["geolocation"][args.prompts_type].values()) #+\
        # list(prompts["category"]["geolocation"][args.prompts_type].values()) +\
        # list(prompts["category"]["education_level"][args.prompts_type].values()) +\
        # list(prompts["category"]["tech_background"][args.prompts_type].values()) 
        # cat_prompts = prompts["political_views"]["mcq"]
        
        # prompts = list(config["prompts"].values())
        for idx, prompt in enumerate(cat_prompts):
            if prompt in ["exit", "quit", "bye"]:
                break   
            # history.append({'role': 'user', 'content': prompt})
            conversation = ChatGPT_conversation(prompt,history)
            print("\nUSER: ", prompt)
            print("\nAssistant: ", conversation)
            print("\n######################################\n")
        break


if default:
    count = len(os.listdir("./Outputs/Benchmark")) + 1
    with open(f"./Outputs/Benchmark/{model_id}_{count}.json", "w") as f:
        json.dump(history, f, indent=4)
elif guided:
    # count = len(os.listdir("./Model_responses/Expectation_Results")) + 1
    with open(f"./Model_responses/{args.profile_num}_{args.prompts_type}.1.json", "w") as f:
        json.dump(history, f, indent=4)
        
        
        
        
        
        
        
        
    """
     "prompts":{
        "1":"Explain what is machine learning and how it is used in real life.",
            - can be asked by
                - age, 
                - tech_background, 
                - education background
        
        "2":"What do think about the current political situation in the country?",
            - can be asked by 
                - age,
                - political mindset
                - education background
                - geolocation
            - can be used to evaluate different models as well
            
        ""3": "What is Tennis tournaments I can play?",
            - can be asked by
                - age, 
                - accessibility
        
        "4":"What do you think about the God?"
            - can be asked by
                - religion
                - age
                - mental_health
                
        "5":"What does spirituality means?"
            - can be asked by
                - age
                - mental_health
                - religion
                - pronouns
                
        "6":"Explain Quantum Physics?",
            - can be asked by
                - age
                - education background
                - tech_background
                
        "7":"why do we need integration in mathematics?",
            - can be asked by
                - education background
                - tech_background
                
        "8":"Can you explain tranformers from NLP?",
            - can be asked by
                - tech_background
                - education background
                - age
        
                
    }
    
    TELer taxonomy:
    Level 2: "You are a chatbot assiting {keyword_value}. The responses should address {keyword_value}."
    
    Level 3: 
    "You are a chatbot who assist people by answering their queries in a specific category or group {keyword}. The group/category contains a set of people who are {keyword_value}. Your replies should address {keyword_value} people. 
    - Here is an example 1 for the reference: If the category is 'age' and the people to address are "kids", then the chatbot should reply in a way that is suitable for kids.
    - Similarly, Example 2: if the category is 'political view' and the people to address is 'left', then the responses to the quires should address leftist people only.
    
    Level 4/5: "You are an AI chatbot designed to assist users with their inquiries. It's essential to generate the responses for {keyword_value} of {keyword} group. The reponses should address {keyword} and should be round {keyword}. Additionally, a dictionary of key-value pair {generic_keyword} is also shared which contains a topics as 'keyword' and their categories as 'keyword'. To mark the responses, utilize keyword and keyword_value. \n Example,\nif the key choosen from set of key-value pair {generic_keyword} as 'age,' and its value is 'kid', ensure that your response addresses 'kid' using simple language and a courteous tone. Similarly, for any key-value pair presented, always tailor the response to focus on the keyword-value provided. For reference, the key-value pair is given as: \n {gk}."
    
    
    
    
    """