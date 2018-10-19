# List of drivers for Backup tasks

### Borg

Driver name: `borg`
List of all options :
 - `pswd`: borg repo password
 - `compression`: same as --compression arg of [borg](https://borgbackup.readthedocs.io/en/stable/usage/create.html).
 - `name`: Backup name, default is `::{hostname}-{date}`.
 - `prune`: what rule use to prune old backup, i.e: `-d 7 -w 4 -m 3 -y 1`. See [prune](https://borgbackup.readthedocs.io/en/stable/usage/prune.html).
 