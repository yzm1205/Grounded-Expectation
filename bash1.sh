#!/bin/bash


USA(){
    for i in {6..21}; do
    python src/run.py -p $i -m gpt4 -pl USA -save True
    # CUDA_VISIBLE_DEVICES=0,1 python src/run.py -p $i -m Llama3 -pl USA -save True
    done
}

India(){
    for i in {0..21}; do
    python src/run.py -p $i -m claude -pl India -save True
    done
}

Bangladesh(){
    for i in {0..21}; do
    python src/run.py -p $i -m gpt4 -pl Bangladesh -save True
    done
}

# echo "USA Profile Running"
# USA 

# echo "India Profile Running"
# India 

echo "Bangladesh Profile Running"
Bangladesh 