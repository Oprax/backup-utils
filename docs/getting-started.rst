==================
 Getting Starting
==================

.. _1.-installation:

1. Installation
===============

You can use pip

.. code:: bash

   pip install backup-utils

You can build the project yourself:

.. code:: bash

   git clone https://gitlab.com/Oprax/backup-utils.git
   cd backup-utils
   make build # will produce a `dist/backup_utils.pyz` file

.. _2.-usage:

2. Usage
========

::

   usage: backup_utils.pyz [-h] [-v] [-r] [-n] [-d DIR]

   Process some integers.

   optional arguments:
     -h, --help         show this help message and exit
     -v, --version      show program's version number and exit
     -r, --run          Create a new backup, default command if no args has given
     -n, --notify       Send a notification to test notifier settings
     -d DIR, --dir DIR  Add a new directory to the backup list, so next run it
                        will be back up

.. _3.-example:

3. Example
==========

.. code:: bash

   backup-utils -d /an/absolute/path -d ./a/relative/path
   backup-utils --dir ~/user/path

   backup-utils --run # the long one
   backup-utils -r # the shortcut
   backup-utils # `run` is the default command if there is no argument

.. _4.-configuration:

4. Configuration
================

The configuration file is a JSON file store in
``~/.config/bak-utils/config.json``.

You can see ``config.example.json`` to have an example.

Root object:

-  ``directories``: A list of directories to backup, please use
   ``--dir`` command to add a new directory.
-  ``repo``: The directory containing the backup and that will be
   synchronized to a remote server.
-  ``backup``, ``sync``, ``database`` and ``notifier`` : are tasks
   objects.

For each tasks object, the most important key is the ``driver``.
``backup``, ``sync`` and ``database`` objects has hooks, which execute a
shell command.

For the moment there are ``pre_hook`` and ``post_hook`` which is
executed before and after each task.

If there is no ``database`` key in the config file, this task will be
skipped.

Database task as a ``backup_directory`` to specify in which directory,
SQL file will be saved.

The other params are depending on the driver. See below for more
details.
