#!/bin/bash

cd src/twitter
python get_users.py

cd ../procrystalline_lattices
./procrystal.x

cd ../twitter
python post_lattices.py
