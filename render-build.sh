#!/bin/bash

# Log: Installing Poppler
echo "Installing Poppler..."
apt-get update && apt-get install -y poppler-utils

# Log: Installing Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
