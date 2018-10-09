Backup Utils
============

The goal of the project is to simplify backup creation. 
At the beggining it's using [BorgBackup](https://www.borgbackup.org/) and [Rclone](https://rclone.org).
Now you can extend it !

# 1. Installation

`make build` and get the the pyz file into dist/

# 2. Usage

There are two commands. 
The first one is for is for add directory to configuration file which would be backup is the next time.

```bash
dist/backup_utils.pyz -d /an/absolute/path -d ./a/relative/path
dist/backup_utils.pyz --dir ~/user/path
```

It is usefull because this command will resolve the path for to have an absolute path.

Ths seconds command is the command to run a backup :

```bash
dist/backup_utils.pyz --run # the long one
dist/backup_utils.pyz -r # the shortcut
dist/backup_utils.pyz # `run` is the default command if there are no argument
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


