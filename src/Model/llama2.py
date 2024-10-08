from typing import Optional
import sys
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from dotenv import load_dotenv
load_dotenv(dotenv_path="./src/.env")

class LLMChat:
    def __init__(self, model_id):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None

    def initialize(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def process_messages(self, messages):
        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)
        return input_ids

    def generate_response(self, input_ids, max_new_tokens=256, temperature=0.6, top_p=0.9):
        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            eos_token_id=terminators,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
        )
        response = outputs[0][input_ids.shape[-1]:]
        return self.tokenizer.decode(response, skip_special_tokens=True)

def main():
    model_id = "/data/shared/llama3-instruct/Meta-Llama-3-8B-Instruct_shard_size_2GB"
    chat = LLMChat(model_id)
    chat.initialize()

    messages = [
        {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
        {"role": "user", "content": "Who are you?"},
    ]

    input_ids = chat.process_messages(messages)
    response = chat.generate_response(input_ids)
    print(response)

if __name__ == "__main__":
    main()


