#!/bin/bash

# Install required dependencies
apt-get update && apt-get install -y poppler-utils

# Ensure Python dependencies are installed
pip install --upgrade pip
pip install -r requirements.txt
