#!/bin/bash

echo "Installing system dependencies..."
apt-get update && apt-get install -y poppler-utils

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete!"
