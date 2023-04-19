#!/bin/bash

# Set up virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run script
python twitter_agent.py
