# List of drivers for Database task

### MySQL

Driver name : `mysql`
Use `mysqldump`, make sure it's install on the server !
List of all options :
 - `extra_file`: path of the .cnf file containing credentials for connection, default: `~/.my.cnf`
 - `database`: list of database to backup
 - `lock_tables`: boolean for the [--lock-tables](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_lock-tables) options, default : `false`
 