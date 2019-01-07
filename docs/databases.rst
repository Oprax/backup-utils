==============================
 List of drivers for Database
==============================

For each database driver:

-  ``backup_directory``: is the directory which store backups file.
-  ``compression``: Compression apply to SQL backup file, choose
   ``gzip``, ``bzip2`` or ``xz``, default is ``null`` (no compression)

MySQL
=====

Driver name: ``mysql`` Use ``mysqldump``, make sure it's installed on
the server! List of all options :

-  ``extra_file``: path of the .cnf file containing credentials for
   connection, default: ``~/.my.cnf``
-  ``database``: list of database to backup
-  ``lock_tables``: boolean for the `--lock-tables`_ options, default :
   ``false``

PostgreSql
==========

Driver name: ``postgre`` Use ``pg_dump``, make sure it's installed on
the server! List of all options :

-  ``database``: list of database object to backup with this parameters :
    -  ``user``: user for database
    -  ``pswd``: Password for database
    -  ``host``: Postgres server address, default to ``localhost``
    -  ``port``: server port, ``5432`` by default.
    -  ``name``: Name of the database

Example:
```
{
    "database": {
        "driver": "postgre",
        "cmd": "pg_dump",
        "backup_directory": "/home/backup/databases",
        "database": [
            {
                "user": "supersite",
                "pswd": "p455w0rd",
                "name": "supersite_db",
            }
        ]
    }
}
```

Sqlite
======

Driver name: ``sqlite`` List of all options :

-  ``database``: list of database file to backup

.. _--lock-tables: https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_lock-tables

