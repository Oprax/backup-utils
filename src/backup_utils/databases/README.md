# List of drivers for Database task

For each database driver:
 - `backup_directory`: is the directory which store backups file.
 - `compression`: Compression apply to SQL backup file, 
                  choose `gzip`, `bzip2` or `xz`, default is `null` (no compression)

### MySQL

Driver name: `mysql`
Use `mysqldump`, make sure it's installed on the server!
List of all options :
 - `extra_file`: path of the .cnf file containing credentials for connection, default: `~/.my.cnf`
 - `database`: list of database to backup
 - `lock_tables`: boolean for the [--lock-tables](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_lock-tables) options, default : `false`


### Sqlite

Driver name: `sqlite`
List of all options :
 - `database`: list of database file to backup
