# provision-ubuntu

Provisions my Ubuntu Linux system using Ansible


## Setup

This repo should be cloned to your `~/code/provision-ubuntu-ansible` directory, like so:

```
git clone https://github.com/yanhan/provision-ubuntu-ansible.git ~/code/provision-ubuntu-ansible
```

It also assumes that you have cloned the dotfiles repo (https://github.com/yanhan/dotfiles) to `~/dotfiles`.

### Configuring the repository

#### ansible/roles/system/vars/main.yml

Open the `roles/system/vars/main.yml` file.

Edit the value of the `home_path` variable to the absolute path of your `$HOME` (check out the `Run` section for an alternative to this).


## Run

```
./run
```

If the path to your home directory is different from the value of the `home_path` variable in `roles/system/vars/main.yml`, run with:

```
./run --extra-vars home_path=/path/to/your/home/dir
```


## License

[3-Clause BSD License](/LICENSE), Copyright (c) 2019 Yan Han Pang
