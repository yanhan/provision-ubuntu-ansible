# provision-ubuntu

Provisions my Ubuntu Linux system using Ansible

## Setup

### Preliminaries

Follow the instructions here to generate an SSH key and add it to your github
account:

    https://help.github.com/articles/generating-ssh-keys/

Then execute the following commands in the top level of this repository:

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

#### ansible/roles/system/files/password.txt

In the `ansible/roles/system/files/password.txt`, there should be a single
line containing the password of your current user.

Note that this file is `.gitignore`d.

This file is necessary for installing the dotfiles; it is used for changing
the shell of the current user to zsh.

## Run

    ansible-playbook -K -i ansible/inventory ansible/localhost.yml

## License

MIT (http://opensource.org/licenses/MIT)
