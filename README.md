# Grounded-Expectation

# [Model Descriptions](https://www.listendata.com/2023/03/open-source-chatgpt-models-step-by-step.html#llama_2)
- Helper links: 
    - [Model desc table](https://deci.ai/blog/list-of-large-language-models-in-open-source/) 
    - [Models Examples](https://huggingface.co/spaces/lmsys/mt-bench)

- LeaderBoard: 
    - [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
    - [Chatbot Arena Leaderboard](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard)
## GPT
- By OpenAI
- Closed Source
### GPT3.5
- Context window
### GPT4
- Context window

## Gemini
- By: Google
- Open Source
- Context window:
- Desc: 
- Link: https://ai.google.dev/models/gemini

## Claude
- By: Anthropic
- Context window : 100K - 200K

## Palm2
- By: Google
- Open Source
- Context window: 

## Falcon
- Open Source
- Context window: 

## Flan-T5
- By: Google
- Open Source
- Context window: 
- Desc: It is multilingual and uses instruction fine-tuning that improves the performance and usability of pretrained language models. It is a variant of T5 that generalises better and outperforms T5 in many Natural Language Processing tasks.

## Mixtral
- By: Mistral
- Open Source
- Context window: Mixtral-8X has 32K 
- Desc: MOE model (mixture of Experts)

## Llama2
- By: Facebook
- Open Source
- Context window: 
- Desc:
- Available size: 7B, 13B and, 70B
- Requirments:
    - GPU:

## Dolly2
- Open Source
- By: Databricks teams
- Desc: Model based EleutherAI's Pythia model and they later fine-tuned on approximately 15,000 record instruction corpus. It comes under Apache 2 license which means the model, the training code, the dataset, and model weights that it was trained with are all available as open source, such that you can make a commercial use of it to create your own customized large language model.
- Context window: 
- Avaliable Sizes: 12B, 7B and 3B parameters.
- Requirments:
     - GPU: -  
        ~10 GB for 7B with 8 Bit quantizations
         ~18 GB for 12B model with 8 Bit quantizations


## Vicuna
- Open Source
- By: Team of researchers from UC Berkeley, CMU, Stanford, and UC San Diego
- Context window: 
- Desc: It was fine tuned on Llama using chat dataset extracted from ShareGPT website. The researchers claimed the model scored more than 90% quality of OpenAI ChatGPT-4. It's worth noting that its performance is almost equal to Bard. They used the training program of Alpaca and improved further on two aspects - multi-round conversations and long sequences.