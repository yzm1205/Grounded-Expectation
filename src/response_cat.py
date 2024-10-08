from textwrap import indent
import pandas as pd
import os
import json
from datasets import Dataset
from tqdm import tqdm
import sys
sys.path.insert(0,"src/")
from myutils import mkdir_p,full_path

country_response_files = ["user_profile_USA","user_profile_Bangladesh","user_profile_India"]
model_list = ["claude","gemini","gpt3","llama3","mistral","phi"]
result_path = "./results_new_v3"

india_path = os.path.join(result_path,country_response_files[2])
usa_path = os.path.join(result_path,country_response_files[1])
bangalesh_path = os.path.join(result_path,country_response_files[0])

# filtered - they are true index, starting from 1
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


# list of models in each country
india = os.listdir(india_path)
usa = os.listdir(usa_path)
bangladesh = os.listdir(bangalesh_path)

def extract_numeric_part(file_name):
    # to avoid lexcial sorting, instead sorting based on profile number
    return int(file_name.split('_')[1].split('_')[0])

def list_json_files(folder_path):
    json_files = []
    get_list = os.listdir(folder_path)
    get_list.sort(key=extract_numeric_part)
    for file_name in get_list:
        if file_name.endswith('.json'):
            json_files.append(file_name)
    return json_files


def cat(country):
    gemini = os.path.join(result_path,f"user_profile_{country}/gemini/")
    Llama3 = os.path.join(result_path,f"user_profile_{country}/llama3/")
    mistral = os.path.join(result_path,f"user_profile_{country}/mistral/")
    phi = os.path.join(result_path,f"user_profile_{country}/phi/")
    gpt3 = os.path.join(result_path,f"user_profile_{country}/gpt3/")
    claude = os.path.join(result_path,f"user_profile_{country}/claude/")
    
    
    total_profiles = len(os.listdir(gemini))
    for profile_num in range(total_profiles):
        with open(f"{gemini}{list_json_files(gemini)[profile_num]}","r") as file:
            gemini_data = json.load(file)
            
        with open(f"{Llama3}{list_json_files(Llama3)[profile_num]}","r") as file:
            Llama3_data = json.load(file)
            
        with open(f"{mistral}{list_json_files(mistral)[profile_num]}","r") as file:
            mistral_data = json.load(file)
            
        with open(f"{phi}{list_json_files(phi)[profile_num]}","r") as file:
            phi_data = json.load(file)      
        
        with open(f"{gpt3}{list_json_files(gpt3)[profile_num]}","r") as file:
            gpt3_data = json.load(file)      
            
        with open(f"{claude}{list_json_files(claude)[profile_num]}","r") as file:
            claude_data = json.load(file)      
            
        # common user profile
        user_profile = gemini_data["user_profile"]  
        
        list_of_attr = list(gemini_data.keys())[3:]   # list of attribute in each profile
        len_of_keys = len(list_of_attr)
        
        df = pd.DataFrame(columns=["User_Profile","Prompt","Response","Adhere to Expectation (1-5)","Quality of Response (1-5)","Hallucination (1-5)"])
        # for each key
        count=0
        for attr in list_of_attr:
            if attr == "tech background":
                attr_ = "tech_background_"
            else:
                attr_ = attr + "_"
            for que_num in range(len(gemini_data[attr])):
                question = gemini_data[attr][que_num]["user"]
                
                
                assert question == claude_data[attr][que_num]["user"], "claude prompt does not match"
                claude_response = claude_data[attr][que_num]["assistant"]
               
                assert question == gemini_data[attr][que_num]["user"], "gemini prompt does not match"
                gemini_response = gemini_data[attr][que_num]["assistant"]
                
                assert question == gpt3_data[attr][que_num]["user"], "gpt3 prompt does not match"
                gpt3_response = gpt3_data[attr][que_num]["assistant"]
                
                assert question == Llama3_data[attr][que_num]["user"], "LLama3 prompt does not match"
                Llama3_response = Llama3_data[attr][que_num]["assistant"]
                
                assert question == mistral_data[attr][que_num]["user"], "Mistral prompt does not match"
                mistral_response = mistral_data[attr][que_num]["assistant"]
                
                assert question == phi_data[attr][que_num]["user"], "phi prompt does not match"
                phi_response = phi_data[attr][que_num]["assistant"]
                
                # Model
                # df.at[count,"Model"] = "gpt3"
                # df.at[count+1,"Model"] = "Llama3"
                # df.at[count+2,"Model"] = "Mistral"
                # df.at[count+3,"Model"] = "Claude"
                # df.at[count+4,"Model"] = "Gemini"
                # df.at[count+5,"Model"] = "Phi"
                # df.at[count+6,"."] = "."
                
                
                # User Profile
                df.at[count,"User_Profile"] = f"{user_profile}"  
                df.at[count+1,"User_Profile"] = "."
                df.at[count+2,"User_Profile"] = "."
                df.at[count+3,"User_Profile"] = "."
                df.at[count+4,"User_Profile"] = "."
                df.at[count+5,"User_Profile"] = "."
                df.at[count+6,"."] = "."
                
                
                
                #prompt
                df.at[count,"Prompt"] = question
                df.at[count+1,"Prompt"] = "."
                df.at[count+2,"Prompt"] = "."
                df.at[count+3,"Prompt"] = "."
                df.at[count+4,"Prompt"] = "."
                df.at[count+5,"Prompt"] = "."
                df.at[count+6,"."] = "."
                
                
                
                # Model Responses
                df.at[count,"Response"] = gpt3_response
                df.at[count+1,"Response"] = Llama3_response
                df.at[count+2,"Response"] = mistral_response
                df.at[count+3,"Response"] = claude_response
                df.at[count+4,"Response"] = gemini_response
                df.at[count+5,"Response"] = phi_response
                df.at[count+6,"."] = "."
        
                count += 7

        
        save_path = mkdir_p(f"{result_path}/Aggregated_response/{country}_responses_v2.xlsx")
        if os.path.exists(save_path):
            with pd.ExcelWriter(save_path, mode ="a",if_sheet_exists='overlay') as write:
                df.to_excel(write,sheet_name=f"Profile_{profile_num}")
        else:
            df.to_excel(save_path,sheet_name=f"Profile_{profile_num}",header=True,
                        merge_cells=True)
    
        
    
if __name__ == "__main__":
    # cat("USA")
    # cat("India")
    cat("Bangladesh")
    print("done")
        
                
                
                
        
    
    
"""
pronoun = [1,2,7,8,9]
political_views = [2,4,5,7,9]
religious_veiws = [1,3,5,6,7]
geolocation = [1,2,4,7,10]
education_level = [1,5,6,7,10]
tech background = [2,3,4,5,7]
mental_health = [1,2,3,4,6]
accessibility = [1,2,3,7,13]
age_group = [1,2,4,5,9]
financial_status = [3,6,7,10,12]
"""
    
    
