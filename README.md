Backup Utils
============


[![pipeline status](https://gitlab.com/Oprax/backup-utils/badges/master/pipeline.svg)](https://gitlab.com/Oprax/backup-utils/commits/master)
[![PyPI - License](https://img.shields.io/pypi/l/backup-utils.svg)](https://gitlab.com/Oprax/backup-utils/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


The goal of the project is to simplify backup creation. 
At the beggining it's using [BorgBackup](https://www.borgbackup.org/) and [Rclone](https://rclone.org).
Now you can extend it !

# 1. Installation

You can use pip

```bash
pip install backup-utils
```

You can build the project yourself:

```bash
git clone https://gitlab.com/Oprax/backup-utils.git
cd backup-utils
make build # will produce a `dist/backup_utils.pyz` file
```

# 2. Usage

There are two commands. 
The first one is for is for add directory to configuration file which would be backup is the next time.

```bash
backup-utils -d /an/absolute/path -d ./a/relative/path
backup-utils --dir ~/user/path
```

It is usefull because this command will resolve the path for to have an absolute path.

Ths seconds command is the command to run a backup :

```bash
backup-utils --run # the long one
backup-utils -r # the shortcut
backup-utils # `run` is the default command if there are no argument
```

# 3. Configuration

The configuration file is a JSON file store in `~/.config/bak-utils/config.json`.

You can see `config.example.json` to have an example.

Root object:
 - `directories`: A list of directories to backup, please use `--dir` command to add a new directory.
 - `repo`: The directory containing the backup and that will be synchronize to a remote server.

For `backup`, `sync` and `database` object, the most important is the `driver` key.
The other params is depending the driver.

`backup` driver supported:
 - `borg`

`sync` driver supported:
 - `rclone`

`database` driver supported:
 - `mysql`

If there is no `database` key in the config file, this task will be skipped.


