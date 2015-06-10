# About

Provisions my Ubuntu Linux system using Ansible

## Setup

### Preliminaries

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

### Configuring the repository

#### ansible/roles/system/vars/main.yml

Open the `ansible/roles/system/vars/main.yml` file.

Edit the value of the `home_path` variable to the absolute path of your `$HOME`.

Edit the value of the `repo_files_path` variable to the absolute path of the
`ansible/roles/system/files` folder in this repository.

Edit the `dotfiles_repo_path` variable to the absolute path of the
[dotfiles repository](https://github.com/yanhan/dotfiles).

#### ansible/localhost.yml

Open the `ansible/localhost.yml` file.

Edit the value of the `user` variable to your actual username.

## Run

    ansible-playbook -K -i ansible/inventory ansible/localhost.yml
