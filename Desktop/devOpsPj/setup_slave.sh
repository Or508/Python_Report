#!/bin/bash

# Setup script for Jenkins Linux Slave
# This script installs necessary dependencies: Java 17, Git, and Python3

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Java 17 (JRE)
echo "Installing OpenJDK 17..."
sudo apt-get install -y openjdk-17-jre-headless

# Install Git
echo "Installing Git..."
sudo apt-get install -y git

# Install Python3
echo "Installing Python3..."
sudo apt-get install -y python3 python3-pip

# Verify installations
echo "--- Verification ---"
java -version
git --version
python3 --version

echo "Setup complete. The machine is ready to be added as a Jenkins agent."
