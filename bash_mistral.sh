#!/bin/bash

USA(){
    for i in {0..21}; do
    CUDA_VISIBLE_DEVICES=2,3 python src/run.py -p $i -m mistral -pl USA
    done
}

India(){
    for i in {0..21}; do
    CUDA_VISIBLE_DEVICES=2,3 python src/run.py -p $i -m mistral -pl India
    done
}

Bangladesh(){
    for i in {0..21}; do
    CUDA_VISIBLE_DEVICES=2,3 python src/run.py -p $i -m mistral -pl Bangladesh
    done
}

echo "USA Profile Running"
USA 

echo "India Profile Running"
India 

echo "India Profile Running"
Bangladesh 