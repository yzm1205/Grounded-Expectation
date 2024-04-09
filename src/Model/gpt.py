import os
import json
from openai import OpenAI
import yaml
from argparse import ArgumentParser
from dotenv import load_dotenv
load_dotenv(dotenv_path="./src/.env")


class GPT3Model:
    
    def __init__(self,sysetm_role,model_name='gpt-3.5-turbo-0125'):
    
        self.client = OpenAI(api_key=os.getenv("gpt3_key"))
        self.model_name = model_name
        self.sys_role = sysetm_role
        

    def generate_text(self, prompt, max_tokens=256, temperature=1, top_p=1.0):
        """
        Generate text using the GPT-3 model.

        Args:
            prompt (str): The prompt to use for text generation.
            max_tokens (int): The maximum number of tokens to generate. Defaults to 100.
            temperature (float): The temperature to use for text generation. Defaults to 0.7.
            top_p (float): The top-p value to use for text generation. Defaults to 1.0.
            n (int): The number of completions to generate. Defaults to 1.

        Returns:
            list: A list of generated text outputs.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", 
                    "content": self.sys_role},
                    {"role":"user",
                    "content": prompt }],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content


if __name__ == "__main__":
# Example usage
    profile = "Gen-Y"
    system_content= f"You are a chat bot assiting people with their queries. The responses should be genereated for the user profile as {profile}. Note that, the repsonses should align with the user profile. For instance, example 1: If the user profile has 'age' keyword and its value is 'age' and the people to address are 'kids', then the chatbot should reply in a way that is suitable for kids. -  Similarly, Example 2: if the user profile has'political view' category and if its value is 'left wing', then the responses to the quires should address leftist people only. - Example 3: In the user profile, there could be multiple keywords such as 'age', political_view' and many more and its value could be 'adult', leftist' respectively. The keywords and its values define the user profile. So, generate responses such that it only intereset to that user profile."

    model = GPT3Model(sysetm_role=system_content)
    prompt = "What is the purpose of life?"
    generated_text = model.generate_text(prompt)
    print(generated_text)