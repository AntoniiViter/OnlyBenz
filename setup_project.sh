#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Creating one now..."
    python3 -m venv venv
    exit 1
fi

# Activate the virtual environment
source venv/bin/activate

# Navigate to the project directory (relative path)
cd "$(dirname "$0")"

# Install dependencies from requirements.txt
pip install -r app/requirements.txt

# Deactivate virtual environment
deactivate

