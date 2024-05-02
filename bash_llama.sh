#!/bin/bash


USA(){
    for i in {0..21}; do
    CUDA_VISIBLE_DEVICES=0,1 python src/run.py -p $i -m Llama3 -pl USA
    done
}

India(){
    for i in {3..21}; do
    CUDA_VISIBLE_DEVICES=0,1 python src/run.py -p $i -m Llama3 -pl India
    done
}

Bangladesh(){
    for i in {0..21}; do
    CUDA_VISIBLE_DEVICES=0,1 python src/run.py -p $i -m Llama3 -pl Bangladesh
    done
}

# echo "USA Profile Running"
# USA 

echo "India Profile Running"
India 

echo "India Profile Running"
Bangladesh 