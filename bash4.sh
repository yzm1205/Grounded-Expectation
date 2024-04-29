#!/bin/bash

echo "Running Script"
for ((i = 0; i < 22; i++)); do
    echo "Processing : Profile_$i"


    echo "Phi-Bangladesh model Running.... \n"
    python src/run.py  -p $i -pt general_questions -m phi -cuda 1 -lv 4 -pl Bangladesh || true
    # python src/run.py  -p $i -pt general_questions -m gemini -lv 1|| true

done

for ((i = 0; i < 22; i++)); do
    echo "Processing : Profile_$i"


    echo "Gemini-Bangladesh model Running.... \n"
    python src/run.py  -p $i -pt general_questions -m phi -cuda 1 -lv 4 -pl India || true
    # python src/run.py  -p $i -pt general_questions -m gemini -lv 1|| true

done
