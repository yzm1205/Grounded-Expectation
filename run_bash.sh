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

for ((i = 0; i < 20; i++)); do
    echo "Processing : Profile_$i"
    python src/run.py  -p $i -pt general_questions -m gpt3 || true
    python src/run.py  -p $i -pt general_questions -m claude || true
    python src/run.py  -p $i -pt general_questions -m gemini || true

done
