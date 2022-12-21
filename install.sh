#!/usr/bin/env bash
# This install script downloads python3 and pip3 if necessary, it also sets up
# the project's python virtualenv and installs the necessary python modules.
# Written by John R., Dec. 2022.

# Strict mode, close on any non-zero exit status.
set -eo pipefail

# Could break system python if pip is run as root.
if [[ "$EUID" -eq 0 ]]; then
    echo 'Do NOT run this script as root!'
    exit 1
fi

echo '####### Pulling in apt updates...'
sudo apt update

if ! which python3; then
    echo '####### Installing `python3`...'
    sudo apt install -y python3
fi

if ! which pip3; then
    echo '####### Installing `pip3`...'
    sudo apt install -y python3-pip
    echo '####### Upgrading `pip3`...'
    python3 -m pip install --upgrade pip
fi

if ! python3 -c "import virtualenv"; then
    echo '####### Installing `virtualenv`...'
    python3 -m pip install --user virtualenv
fi

echo '####### Setting up Virtual Env...'
python3 -m virtualenv venv
source venv/bin/activate

echo '####### Install Requirements...'
python3 -m pip install -r requirements.txt

echo '####### Project Setup & Installation Complete!!!'
echo 'Run, `source venv/bin/activate` to start the python virtual environment.'
