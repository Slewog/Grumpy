#!/bin/bash
env_name="grumpy_env"

python3 -m venv $env_name

source $env_name/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

python3 main.py
