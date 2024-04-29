#!/bin/bash

echo "Running Script"
# python src/gpt_prompt.py  -p profile_9 -pt general_questions
# python src/gpt_prompt.py  -p profile_10 -pt general_questions
# python src/gpt_prompt.py  -p profile_11 -pt general_questions
# python src/gpt_prompt.py  -p profile_12 -pt general_questions
# python src/gpt_prompt.py  -p profile_13 -pt general_questions
# python src/gpt_prompt.py  -p profile_15 -pt general_questions
# python src/gpt_prompt.py  -p profile_15 -pt general_questions

#profiles= "./config/user_profile.json"

# if [! -f "$profiles"]; then
#     echo "File not found!"
#     exit 1
# fi

# # Read the JSON file and extract keys
# keys=($(jq -r 'keys[]' "$profiles"))

# for ((i = 0; i < 9; i++)); do
#     echo "Processing : Profile_$i"

#     # python src/run.py  -p $i -pt general_questions -m claude || true
    
#     # echo "Level 2 prompting \n"
#     # python src/run.py  -p $i -pt general_questions -m gpt3 -lv 2 || true
#     # python src/run.py  -p $i -pt general_questions -m gemini -lv 2|| true

#     # echo "Level 3 prompting \n"
#     # python src/run.py  -p $i -pt general_questions -m gpt3 -lv 3 || true
#     # python src/run.py  -p $i -pt general_questions -m gemini -lv 3|| true

#     # echo "Level 4 prompting \n"
#     # python src/run.py  -p $i -pt general_questions -m gpt3 -lv 4 || true
#     # python src/run.py  -p $i -pt general_questions -m gemini -lv 4|| true
#     echo "GPT4-india model Running.... \n"
#     python src/run.py  -p $i -pt general_questions -m gpt4 -lv 4 -pl India || true

# done

for ((i = 0; i < 22; i++)); do
    echo "Processing : Profile_$i"


    echo "Gemini-India model Running.... \n"
    python src/run.py  -p $i -pt general_questions -m gemini -lv 4 -pl India || true
    # python src/run.py  -p $i -pt general_questions -m gemini -lv 1|| true

done
