# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# class Mistral:
#     def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.2",device="cuda"):
#         self.device = device
#         self.model = AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=torch.bfloat16,device=self.device)
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)

#     def generate(self, messages):
#         conversation = [{"role": "user", "content": "What's the weather like in Paris?"}]
#         # format and tokenize the tool use prompt
#         inputs = self.tokenizer.apply_chat_template(
#                     conversation,
#                     add_generation_prompt=True,
#                     return_dict=True,
#                     return_tensors="pt",
#         )

#         inputs.to(self.model.device)
#         outputs = self.model.generate(**inputs, max_new_tokens=1000)
#         return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


# if __name__ == "__main__":
#     # Example usage
#     model_name = "mistralai/Mistral-7B-Instruct-v0.3"
#     device = "cuda:3" # the device to load the model onto

#     # model_name = "/data/shared/llm_cache/models--mistralai--Mistral-7B-Instruct-v0.1"

#     messages = [
#     {"role": "user", "content": "What is your favourite condiment?"},
#     {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
#     {"role": "user", "content": "Do you have mayonnaise recipes?"}
#     ]
#     mistral = Mistral(model_name,device=device)
#     response = mistral.generate(messages)
#     print(response)

from transformers import pipeline

import os
# os.environ['HF_HOME'] = '/data/shared/llm_cache/models/mistralai/'
class Mistral:
    def __init__(self, model_name="mistralai/Mistral-7B-Instruct-v0.3", system_role="",device="cuda"):
        self.chatbot = pipeline("text-generation", model=model_name,device=device)
        self.system_role = system_role

    def generate(self, prompt):
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt},
        ]
        return self.chatbot(messages,max_length=1024)[0]["generated_text"][2]["content"]
    



if __name__ == "__main__":
    # Example usage
    # model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    model_name = "/data/shared/mistralv3/Mistral-7B-Instruct-v0.3_shard_size_2GB"
    system_role = "I am a chatbot assistant. I can help you with a variety of tasks. How can I assist you today?"

    prompt = "What is your favourite condiment?"
    mistral = Mistral(model_name, system_role)
    response = mistral.generate(prompt)
    print(response)