#!/bin/bash

cd src/twitter
python get_tweets.py 5 2 

cd ../procrystalline_lattices
./procrystal.x

cd ../twitter
python post_lattices.py
