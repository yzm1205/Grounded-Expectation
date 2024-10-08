# from transformers import AutoTokenizer, OlmoForCausalLM, AutoModelForCausalLM, AutoTokenizer
# from hf_olmo import *
# from ai2_olmo import OLMoTokenizer, OLMoForCausalLM, OLMoTokenizerFast
from hf_olmo import OLMoForCausalLM, OLMoTokenizerFast
import torch

class OLMo:
    def __init__(self,model_name = "allenai/OLMo-7B",system_prompt ="",device="cuda") -> None:
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.tokenizer = OLMoTokenizerFast.from_pretrained(model_name,trust_remote_code=True)
        self.model = OLMoForCausalLM.from_pretrained(model_name,device_map="auto",torch_dtype=torch.float16, load_in_8bit=True)
        
    def generate_response(self,prompt, max_new_tokens=100):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        formatted_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False,add_generation_prompt=True)
        inputs = self.tokenizer.encode(formatted_prompt, return_tensors="pt",add_special_tokens=False)
        outputs = self.model.generate(inputs.to(self.model.device), max_new_tokens=max_new_tokens,do_sample=True, top_k=50, top_p=0.95)
        # outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        # return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    olmo_path = "/data/shared/olmo-instruct/OLMo-7B-0724-Instruct-hf_shard_size_2GB"
    olmo_path2 = "/data/shared/olmo-instruct/OLMo-7B-0724-Instruct-hf_shard_size_1GB"
    olmo_path3= "allenai/OLMo-7B-Instruct"
    
    system_prompt = "You are a helpful assistant. Answer concisely and accurately."
    model = OLMo(model_name= olmo_path3,device=device,system_prompt=system_prompt)
    user_prompt = "What is the capital of France?"
    response = model.generate_response(user_prompt)
    print(response)


