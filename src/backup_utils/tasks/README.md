# List of drivers for Backup tasks

### Borg

Driver name: `borg`
List of all options :
 - `pswd`: borg repo password
 - `compression`: same as --compression arg of [borg](https://borgbackup.readthedocs.io/en/stable/usage/create.html).
 - `name`: Backup name, default is `::{hostname}-{date}`.
 - `prune`: what rule use to prune old backup, i.e: `-d 7 -w 4 -m 3 -y 1`. See [prune](https://borgbackup.readthedocs.io/en/stable/usage/prune.html).


### Tar

Driver name: `tar`
Archive file is creating under `repo` directory.
List of all options :
 - `name`: Archive name, default is `{hostname}-{date}.tar.gz`.
 - `compression`: Compression use by tar must be one of `gzip`, `bzip2` or `xz`. If no compression is given, try to guess from archive file extension.
