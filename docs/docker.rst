======
Docker
======

You can run backup-utils from docker with the `oprax/backup-utils` image.

You need to bind the volume to access the data you want to back up and to access the configuration.

Attention, the path given in the configuration file will be relative to the docker's file system!


Example::

    docker run -it -v config.json:/root/.config/bak-utils/config.json -v /opt/borgrepo:/opt/borgrepo oprax/backup-utils backup-utils --run
