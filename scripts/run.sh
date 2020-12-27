#!/bin/bash

export PROCRYSTAL_DIR=XXX

cd $PROCRYSTAL_DIR

source activate con3

cd ../src/twitter
python get_tweets.py 3 1 

cd ../procrystalline_lattices
./procrystal.x

cd ../twitter
python post_lattices.py
