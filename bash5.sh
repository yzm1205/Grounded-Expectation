#!/bin/bash

echo "Running Script"
for ((i = 0; i < 22; i++)); do
    echo "Processing : Profile_$i"


    echo "Phi-USA model Running.... \n"
    python src/run.py  -p $i -pt general_questions -m phi -cuda 2 -lv 4 -pl USA || true
    # python src/run.py  -p $i -pt general_questions -m gemini -lv 1|| true

done


