import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

torch.random.manual_seed(0)

class phi3mini:
    def __init__(self,system_role,cuda_device=0):
        self.system_role = system_role
        self.cuda = cuda_device
        
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-128k-instruct", 
            device_map=f'cuda:{self.cuda}', 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

    def generate_response(self, prompt, max_tokens=500, temperature=1):
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt},
        ]

        

        generation_args = {
            "max_new_tokens": max_tokens,
            "return_full_text": False,
            "temperature": temperature,
            "do_sample": False,
        }

        output = self.pipe(messages, **generation_args)
        # print(output[0]['generated_text'])
        return output[0]['generated_text']
    
if __name__ == "__main__":
    profile = "Gen-Y"
    system_content= f"You are a chat bot assiting people with their queries. The responses should be genereated for the user profile as {profile}. Note that, the repsonses should align with the user profile. For instance, example 1: If the user profile has 'age' keyword and its value is 'age' and the people to address are 'kids', then the chatbot should reply in a way that is suitable for kids. -  Similarly, Example 2: if the user profile has'political view' category and if its value is 'left wing', then the responses to the quires should address leftist people only. - Example 3: In the user profile, there could be multiple keywords such as 'age', political_view' and many more and its value could be 'adult', leftist' respectively. The keywords and its values define the user profile. So, generate responses such that it only intereset to that user profile."

    model = phi3mini(system_role=system_content)
    prompt = "What is the purpose of life?"
    generated_text = model.generate_response(prompt)
    print("___________")
    print(generated_text)