# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


PATH = "/data/yash/gemma2/gemma-2-9b_shard_size_2GB"
tokenizer = AutoTokenizer.from_pretrained(PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    PATH,
    device_map="auto",
)

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

outputs = model.generate(**input_ids, max_new_tokens=32)
print(tokenizer.decode(outputs[0]))
