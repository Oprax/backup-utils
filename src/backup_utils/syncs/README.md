# List of drivers for Sync task

### Rclone

Driver name: `rclone`
List of all options :
 - `dist`: name of the distant repo, i.e: `s3:backup/{hostname}` with hostname as a variable.


### Rsync

Driver name: `rsync`
List of all options :
 - `dist`: name of the distant repo, i.e: `backup@example.org:~/{hostname}` with hostname as a variable.
 - `delete`: Boolean to use --delete [flag](https://linux.die.net/man/1/rsync), default to `false`.
 - `excludes`: List of excluding files, or if a string, file name send to `--exclude-from` flag. Optional.
 - `ssh_opts`: SSH options, i.e: `ssh -p 2222` to change port.
 