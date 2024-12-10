FROM --platform=linux/amd64 mcr.microsoft.com/vscode/devcontainers/base:ubuntu-24.04

RUN apt-get update \
    # Install additional OS packages.
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y portaudio19-dev python3-pyaudio \
    # Clean up.
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
