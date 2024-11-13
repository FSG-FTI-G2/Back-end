#!/bin/bash

# Set default versions if not provided
DEFAULT_DOCKER_VERSION="latest"
DEFAULT_NVIDIA_TOOLKIT_VERSION="1.12.1"

# Prompt for versions with default values
read -p "Enter Docker version (default: $DEFAULT_DOCKER_VERSION): " DOCKER_VERSION
DOCKER_VERSION=${DOCKER_VERSION:-$DEFAULT_DOCKER_VERSION}

read -p "Enter NVIDIA Container Toolkit version (default: $DEFAULT_NVIDIA_TOOLKIT_VERSION): " NVIDIA_TOOLKIT_VERSION
NVIDIA_TOOLKIT_VERSION=${NVIDIA_TOOLKIT_VERSION:-$DEFAULT_NVIDIA_TOOLKIT_VERSION}

# Function to install Docker
install_docker() {
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo "Docker installed successfully."
}

# Function to install NVIDIA Container Toolkit
install_nvidia_toolkit() {
    echo "Installing NVIDIA Container Toolkit version $NVIDIA_TOOLKIT_VERSION..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt update
    sudo apt install -y nvidia-container-toolkit=$NVIDIA_TOOLKIT_VERSION*
    sudo systemctl restart docker
    echo "NVIDIA Container Toolkit installed successfully."
}

# Check if Docker is installed and install if necessary
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    install_docker
else
    echo "Docker is already installed."
fi

# Check if NVIDIA Container Toolkit is installed with the specified version
NVIDIA_TOOLKIT_INSTALLED_VERSION=$(dpkg -l | grep nvidia-container-toolkit | awk '{print $3}')
if [[ "$NVIDIA_TOOLKIT_INSTALLED_VERSION" != "$NVIDIA_TOOLKIT_VERSION" ]]; then
    echo "NVIDIA Container Toolkit version $NVIDIA_TOOLKIT_VERSION is not installed. Installing..."
    install_nvidia_toolkit
else
    echo "NVIDIA Container Toolkit version $NVIDIA_TOOLKIT_VERSION is already installed."
fi