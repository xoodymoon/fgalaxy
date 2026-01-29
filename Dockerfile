# Use a lightweight Ubuntu image
FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies needed for the installer
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create a test user (since running as root is too easy)
RUN useradd -m tester && echo "tester:tester" | chpasswd && adduser tester sudo
RUN echo "tester ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER tester
WORKDIR /home/tester

# This command runs your installer directly from your GitHub when the container starts
CMD curl -sSL https://raw.githubusercontent.com/xoodymoon/fgalaxy/main/install.sh | bash && bash
