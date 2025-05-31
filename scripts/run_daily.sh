#!/bin/bash

# Change to the root directory of the project
cd "$(dirname "$0")"/..

# Run the main pipeline
echo "Running DMARC daily job..."
python3 main.py

