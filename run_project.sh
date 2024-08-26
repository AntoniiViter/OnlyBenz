#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Please create one first."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Navigate to the project directory (relative path)
cd "$(dirname "$0")"

# Run the Django development server
uvicorn app.main:app --reload

# Deactivate virtual environment after stopping the server
deactivate