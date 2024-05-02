import pandas as pd
import os
import json



country_response_files = ["user_profile_Bangladesh","user_profile_USA","user_profile_India"]
model_list = ["gemini","Llama3","mistral","phi"]
result_path = "./results"

india_path = os.path.join(result_path,country_response_files[2])
usa_path = os.path.join(result_path,country_response_files[1])
bangalesh_path = os.path.join(result_path,country_response_files[0])


# list of models in each country
india = os.listdir(india_path)
usa = os.listdir(usa_path)
bangladesh = os.listdir(bangalesh_path)

def list_json_files(folder_path):
    json_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            json_files.append(file_name)
    return json_files


def cat(country):
    gemini = os.path.join(result_path,f"user_profile_{country}/gemini/")
    Llama3 = os.path.join(result_path,f"user_profile_{country}/Llama3/")
    mistral = os.path.join(result_path,f"user_profile_{country}/mistral/")
    phi = os.path.join(result_path,f"user_profile_{country}/phi/")
    
    for profile_num in range(22):
        with open(list_json_files(gemini)[profile_num],"r") as file:
            gemini_data = json.load(file)
            
        with open(list_json_files(Llama3)[profile_num],"r") as file:
            Llama3_data = json.load(file)
            
        with open(list_json_files(mistral)[profile_num],"r") as file:
            mistral_data = json.load(file)
            
        with open(list_json_files(phi)[profile_num],"r") as file:
            phi_data = json.load(file)      
            
        # common user profile
        user_profile = gemini_data[0][0]["user_profile"]  
        
        list_of_keys = list(gemini_data[0][1].keys())   # list of attribute in each profile
        len_of_keys = len(list_of_keys)
        
        df = pd.DataFrame(columns=["Question","Responses","Adhere to Exceptation (1-5)","Quality of Response (1-5)","Hallucination (1-5)"])
        # for each key
        for key in list_of_keys:
            for que in range(len(key)):
                # for each question, response for a llm
                question = gemini_data[0][0][key[que]["user"]]
                gemini_response = gemini_data[0][0][key[que]["assistant"]]
                Llama3_response = Llama3_data[0][0][key[que]["assistant"]]
                mistral_response = mistral_data[0][0][key[que]["assistant"]]
                phi_response = phi_data[0][0][key[que]["assistant"]]
                
                
                
        # create a dataframe
        # append all the respsones for each profile each model and each questions
        # save the profile in annotation folder
        
                
                
                
        
    
    
    
    
    
