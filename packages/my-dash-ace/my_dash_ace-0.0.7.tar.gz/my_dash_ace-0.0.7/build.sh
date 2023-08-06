#!/bin/sh

npm run build
rm -rf dist/*
python setup.py clean
#python setup.py sdist
pip install .
