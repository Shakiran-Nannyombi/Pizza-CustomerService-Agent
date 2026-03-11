# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/python:3.10

# Remove problematic Yarn repository (GPG key issue causes apt-get update to fail)
RUN rm -f /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/yarn.sources 2>/dev/null || true

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

# Install Node.js (using NodeSource for latest LTS)
#RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash && \
#    apt-get install -y nodejs

# Verify installs
# RUN az version && node --version && npm --version
