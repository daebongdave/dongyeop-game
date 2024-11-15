#!/bin/bash
# Install Python
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
pyenv install 3.11.0
pyenv global 3.11.0

# Install dependencies
python -m pip install --upgrade pip
pip install pygbag

# Build
pygbag .