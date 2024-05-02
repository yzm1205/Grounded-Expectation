#!/bin/bash

USA(){
    for i in {0..21}; do
    # CUDA_VISIBLE_DEVICES=2,3 python src/run.py -p $i -m mistral -pl USA -save True
    python src/run.py -p $i -m claude -pl USA -save True

    done
}

India(){
    for i in {0..21}; do
    python src/run.py -p $i -m claude -pl India -save True
    done
}

Bangladesh(){
    for i in {0..21}; do
    python src/run.py -p $i -m claude -pl Bangladesh -save True
    done
}

echo "USA Profile Running"
USA 

echo "India Profile Running"
India 

# echo "India Profile Running"
# Bangladesh 