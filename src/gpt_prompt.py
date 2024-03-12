import os
import json
import openai
from dotenv import load_dotenv
load_dotenv()



openai.api_key = "gpt3_key"
print("GPT-3.5-turbo-0125: Running...")


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0125",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )

