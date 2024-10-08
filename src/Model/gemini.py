import google.generativeai as genai
import os
from dotenv import load_dotenv
from sympy import Ge
load_dotenv(dotenv_path="./src/.env")


helper  ="https://ai.google.dev/tutorials/python_quickstart"

class GeminiModel:
    def __init__(self,system_role,model_name = "gemini-1.0-pro"):
        genai.configure(api_key=os.getenv("gemini_key"))
        self.model_name = model_name
        self.sys_role = system_role
        # system_instruction is introducted to gemini 1.5 pro model
        # self.model = genai.GenerativeModel(model_name,system_instruction=self.sys_role) 
        self.model = genai.GenerativeModel(model_name) 
        
        print(f"Gemini-{model_name} model is loaded successfully")

    def generate_response(self,prompt):
        safety_settings = [ 
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"}, 
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
        response = self.model.generate_content(self.sys_role + prompt,
                                               generation_config={'temperature': 1, 'max_output_tokens': 4096},
                                               safety_settings=safety_settings)
        return response.text
    
if __name__ == "__main__":
    profile = "Gen-Y"
    system_content= f"You are a chat bot assiting people with their queries. The responses should be genereated for the user profile as {profile}. Note that, the repsonses should align with the user profile. For instance, example 1: If the user profile has 'age' keyword and its value is 'age' and the people to address are 'kids', then the chatbot should reply in a way that is suitable for kids. -  Similarly, Example 2: if the user profile has'political view' category and if its value is 'left wing', then the responses to the quires should address leftist people only. - Example 3: In the user profile, there could be multiple keywords such as 'age', political_view' and many more and its value could be 'adult', leftist' respectively. The keywords and its values define the user profile. So, generate responses such that it only intereset to that user profile."
    
    model = GeminiModel(system_role=system_content)
    response = model.generate_response("What is purpose of life?")

    print(response)