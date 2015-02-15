# About

Uses ansible to provision an Ubuntu based Linux system

## Setup

Follow the instructions here to generate an SSH key and add it to your github
account:

    https://help.github.com/articles/generating-ssh-keys/

Then execute the following commands:

    # Add the git-core ppa for a more modern version of git
    sudo add-apt-repository ppa:git-core/ppa
    sudo apt-get update
    sudo apt-get install python-virtualenv python-dev
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Run

    ansible-playbook -K -i ansible/inventory ansible/localhost.yml
