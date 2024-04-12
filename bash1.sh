#!/bin/bash

echo "Running Script"
for ((i = 0; i < 20; i++)); do
    echo "Processing : Profile_$i"

    # python src/run.py  -p $i -pt general_questions -m claude || true
    echo "Level 0 prompting \n"
    python src/run.py  -p $i -pt general_questions -m gpt3 -lv 0 || true
    python src/run.py  -p $i -pt general_questions -m gemini -lv 0|| true

    echo "Level 1 prompting \n"
    python src/run.py  -p $i -pt general_questions -m gpt3 -lv 1 || true
    python src/run.py  -p $i -pt general_questions -m gemini -lv 1|| true


done
