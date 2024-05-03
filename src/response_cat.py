from textwrap import indent
import pandas as pd
import os
import json
from datasets import Dataset


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
    Llama3 = os.path.join(result_path,f"user_profile_{country}/Llama3/")
    mistral = os.path.join(result_path,f"user_profile_{country}/mistral/")
    phi = os.path.join(result_path,f"user_profile_{country}/phi/")
    gpt4 = os.path.join(result_path,f"user_profile_{country}/gpt4/")
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
        
        with open(f"{gpt4}{list_json_files(gpt4)[profile_num]}","r") as file:
            gpt4_data = json.load(file)      
            
        with open(f"{claude}{list_json_files(claude)[profile_num]}","r") as file:
            claude_data = json.load(file)      
            
        # common user profile
        user_profile = gemini_data[0]["user_profile"]  
        
        list_of_attr = list(gemini_data[1].keys())   # list of attribute in each profile
        len_of_keys = len(list_of_attr)
        
        df = pd.DataFrame(columns=["User_Profile","Prompt","Response","Model","Adhere to Exceptation (1-5)","Quality of Response (1-5)","Hallucination (1-5)"])
        profile_response_by_country = []
        # for each key
        count=0
        for attr in list_of_attr:
            profile_response = {}
            for que_num in range(len(gemini_data[1][attr])-1):
                # for each question, response for a llm
                question = gemini_data[1][attr][que_num]["user"]
                gemini_response = gemini_data[1][attr][que_num]["assistant"]
                gpt4_response = gpt4_data[1][attr][que_num]["assistant"]
                claude_response = claude_data[1][attr][que_num]["assistant"]
                try:
                    Llama3_response = Llama3_data[1][attr][que_num]["assistant"]
                except TypeError:
                    Llama3_response = Llama3_data[1][attr][que_num][0]["assistant"]
                except IndexError:
                    Llama3_response = Llama3_data[1][attr][0][que_num]["assistant"]
                mistral_response = mistral_data[1][attr][que_num]["assistant"]
                phi_response = phi_data[1][attr][que_num]["assistant"]
                
                # Model
                df.at[count,"Model"] = "Gpt4"
                df.at[count+1,"Model"] = "Llama3"
                df.at[count+2,"Model"] = "Mistral"
                df.at[count+3,"Model"] = "Claude"
                df.at[count+4,"Model"] = "Gemini"
                df.at[count+5,"Model"] = "Phi"
                df.at[count+6,"."] = "."
                
                
                # User Profile
                df.at[count,"User_Profile"] = json.dumps(user_profile,indent=4)  
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
                df.at[count,"Response"] = gpt4_response
                df.at[count+1,"Response"] = Llama3_response
                df.at[count+2,"Response"] = mistral_response
                df.at[count+3,"Response"] = claude_response
                df.at[count+4,"Response"] = gemini_response
                df.at[count+5,"Response"] = phi_response
                df.at[count+6,"."] = "."
                
                
                count += 7
            
       
        save_path = f"./results/Aggregated_response/{country}_responses.xlsx"
        if os.path.exists(save_path):
            with pd.ExcelWriter(save_path, mode ="a",if_sheet_exists='overlay') as write:
                df.to_excel(write,sheet_name=f"Profile_{profile_num}")
        else:
            df.to_excel(save_path,sheet_name=f"Profile_{profile_num}",header=True,
                        merge_cells=True)
        # with pd.ExcelWriter(save_path,mode="a",if_sheet_exists="overlay") as write:
        #     df.to_excel(write,sheet_name=f"Profile_{profile_num}")
        
            
        # create a dataframe
        # append all the respsones for each profile each model and each questions
        # save the profile in annotation folder
        
if __name__ == "__main__":
    cat("Bangladesh")
    print("done")
        
                
                
                
        
    
    
    
    
    
