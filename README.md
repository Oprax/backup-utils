Backup Utils
============


[![pipeline status](https://gitlab.com/Oprax/backup-utils/badges/master/pipeline.svg)](https://gitlab.com/Oprax/backup-utils/commits/master)
[![PyPI - License](https://img.shields.io/pypi/l/backup-utils.svg)](https://gitlab.com/Oprax/backup-utils/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/backup-utils.svg)](https://pypi.org/project/backup-utils/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


The goal of this project is to create a front to backup program like Borg.
Indeed, Borg is a really great tool for backup,
but I always write a bash script to specify directories I want to save.
I also use Rclone to synchronize my backup to a remote.
And finally I need to backup my database.

There are three steps to backup :
1. Database export
2. Archiving
3. Synchronize

For each step, you can use multiple driver for multiple tool.
Also if something go wrong, all Exceptions are catch to send a notification.

By default, database export use **mysql**, archiving **borg**, and synchronize **rclone**.

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

```
usage: backup_utils.pyz [-h] [-v] [-r] [-n] [-d DIR]

Process some integers.

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      show program's version number and exit
  -r, --run          Create a new backup, default command if no args given
  -n, --notify       Send a notification to test notifier settings
  -d DIR, --dir DIR  Add a new directory to the backup list, so next run it
                     will be backup
```
 
# 3. Example

```bash
backup-utils -d /an/absolute/path -d ./a/relative/path
backup-utils --dir ~/user/path

backup-utils --run # the long one
backup-utils -r # the shortcut
backup-utils # `run` is the default command if there are no argument
```

# 4. Configuration

The configuration file is a JSON file store in `~/.config/bak-utils/config.json`.

You can see `config.example.json` to have an example.

Root object:
 - `directories`: A list of directories to backup, please use `--dir` command to add a new directory.
 - `repo`: The directory containing the backup and that will be synchronize to a remote server.
 - `backup`, `sync`, `database` and `notifier` : are tasks objects.


For each tasks object, the most important key is the `driver`.
`backup`, `sync` and `database` objects has hook, which execute a shell command.
For the moment there are `pre_hook` and `post_hook` which is execute before and after each tasks.
If there is no `database` key in the config file, this task will be skipped.
Database task as a `backup_directory` to specify in which directy, SQL file will be save.
The other params is depending the driver. See below for more details.

# 5. Drivers

**[Drivers for Backup](src/backup_utils/tasks/README.md)**
**[Drivers for Sync](src/backup_utils/syncs/README.md)**
**[Drivers for Database](src/backup_utils/databases/README.md)**
**[Drivers for Notifier](src/backup_utils/notifiers/README.md)**
