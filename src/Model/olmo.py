# from transformers import AutoTokenizer, OlmoForCausalLM
# from hf_olmo import OLMoTokenizerFast
# # from ai2_olmo import OLMoTokenizer, OLMoForCausalLM
# import torch

# class OLMo:
#     def __init__(self,model_name = "allenai/OLMo-7B",device="cuda") -> None:
#         self.model_name = model_name
#         self.tokenizer = OLMoTokenizerFast.from_pretrained(model_name,trust_remote_code=True)
#         self.model = OlmoForCausalLM.from_pretrained(model_name).to(device)
        
#     def generate(self,prompt, system_prompt, max_new_tokens=100):
#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt}
#         ]
#         formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
#         inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
#         outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
#         return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
# if __name__ == "__main__":
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = OLMo(device=device)
#     system_prompt = "You are a helpful assistant. Answer concisely and accurately."
#     user_prompt = "What is the capital of France?"
#     response = model.generate(user_prompt, system_prompt)
#     print(response)