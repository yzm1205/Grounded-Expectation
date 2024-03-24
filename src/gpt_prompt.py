import os
import json
from openai import OpenAI
import yaml

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
    - Mistral
    - Llama2
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

# print("gpt3_key") 
client = OpenAI(api_key=os.getenv("gpt3_key"))
model_id = 'gpt-3.5-turbo-0125'
# model_id = 'gpt-4'

print(f"{model_id} : Running...\n\n")

# with open("./src/config.json", "r") as f:
#     config = json.load(f)

with open("./src/keywords.yaml", "r") as f:
    config = yaml.safe_load(f)
    # print("done")
    
default,guided=False,True



def generate_system_prompt(default=default, guided=guided):
    # generic_keywords = config["generic_keywords"]
    # keyword = "age"
    # keyword_value = "kids"
    #default system context
    if default:
        system_context = config["target_system_context_without_kv"]["1"] 
    elif guided:
        # system_context = config["target_system_context_with_kv"]["5"] 
        # system_context = system_context.replace("{keyword}", keyword)
        # system_context = system_context.replace("{keyword_value}", keyword_value)
        # system_context = system_context.replace("{gk}", f"{generic_keywords}")
        system_context= f"""You are a chatbot who assist people by answering their queries. Use this user profile {config} to respond appropriately. 
        Here is an example 1 for the reference: If the profile contains 'age' and its value as kids, then the people to address are "kids". The chatbot should reply in a way that is suitable for kids. 
        
        # """
    else:
        raise ValueError("Invalid system context")
    
    return system_context
    
system_context = generate_system_prompt(default=default, guided=guided)
history = [{"role": "system", "content": system_context}]


def ChatGPT_conversation(prompt,history=[]):
    keyword = "age"
    keyword_value = "kids"
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
    if guided:
        prompts = input('\n User: ')
        if prompts in ["exit", "quit", "bye"]:
                break   
            # history.append({'role': 'user', 'content': prompt})
        conversation = ChatGPT_conversation(prompts,history)
        # print("\nUSER: ", prompts)
        print("\nAssistant: ", conversation)
        print("\n######################################\n")
    if default:
        prompts = list(config["prompts"].values())
        for idx, prompt in enumerate(prompts):
            if prompt in ["exit", "quit", "bye"]:
                break   
            # history.append({'role': 'user', 'content': prompt})
            conversation = ChatGPT_conversation(prompt,history)
            # print("\nUSER: ", prompt)
            print("\nAssistant: ", conversation)
            print("\n######################################\n")
        break


if default:
    count = len(os.listdir("./Outputs/Benchmark")) + 1
    with open(f"./Outputs/Benchmark/{model_id}_{count}.json", "w") as f:
        json.dump(history, f, indent=4)
elif guided:
    count = len(os.listdir("./Outputs/Expectation_Results")) + 1
    with open(f"./Outputs/Expectation_Results/{model_id}_{count}_policitical_view.json", "w") as f:
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