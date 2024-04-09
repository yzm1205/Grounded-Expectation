from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
  
baseModel = "databricks/dolly-v2-12b"
load_8bit = True  
tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-12b")
model = AutoModelForCausalLM.from_pretrained(baseModel, load_in_8bit=load_8bit, torch_dtype=torch.float16, device_map="auto")
generator = pipeline(task='text-generation', model=model, tokenizer=tokenizer)

print(generator("Python code to remove duplicates from dataframe"))