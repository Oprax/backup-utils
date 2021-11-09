import json
import subprocess

from pathlib import Path

from appdirs import AppDirs

from .tasks import tasks
from .syncs import syncs
from .databases import databases
from .notifiers import notifiers


class Backup:
    """
    Main class which execute all tasks and send notifications in case of an error.
    """

    def __init__(self):
        """
        Get the root path and initialize the configuration.

        .. seealso:: _load_cfg()
        """
        self._dirs = AppDirs(appname="bak-utils")
        self._config = {}
        self._cfg_file = Path(self._dirs.user_config_dir) / "config.json"
        self._load_cfg()

    def _load_cfg(self):
        """
        Load configuration from the JSON configuration file.

        .. seealso:: _save_cfg()
        """
        self._cfg_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not self._cfg_file.is_file():
            self._save_cfg()
        else:
            self._config = json.loads(self._cfg_file.read_text())

    def _save_cfg(self):
        """
        Save configuration to a JSON file.

        .. seealso:: _save_cfg()
        """
        self._cfg_file.write_text(json.dumps(self._config, indent=4))

    def _check(self):
        """
        Check there are no missing settings.
        """
        repo = self._config.get("repo", None)
        if repo is None:
            raise ValueError("Repository must be defined !".format(self._repo))
        self._repo = Path(repo)
        # if not a directory, it can be a remote borg repo
        if not self._repo.is_dir():
            self._repo = repo

    def _database(self):
        """
        Fetch the database driver and launch the task.
        """
        driver = databases(self._config.get("database", {}).get("driver", "mysql"))
        self._database_task = driver(
            repo=str(self._repo), **self._config.get("database", {})
        )
        self._database_task.start()
        self._config.get("directories", []).append(self._database_task.backup_dir)

    def _backup(self):
        """
        Fetch the backup driver and launch the task.
        """
        driver = tasks(self._config.get("backup", {}).get("driver", "Borg"))
        self._backup_task = driver(
            directories=self._config.get("directories", []),
            repo=str(self._repo),
            **self._config.get("backup", {})
        )
        self._backup_task.start()

    def _sync(self):
        """
        Fetch the sync driver and launch the task.
        """
        driver = syncs(self._config.get("sync", {}).get("driver", "Rclone"))
        self._sync_task = driver(repo=str(self._repo), **self._config.get("sync", {}))
        self._sync_task.start()

    def _clean(self):
        """
        Clean files after backups
        """
        if self._config.get("database", None):
            self._database_task.clean()

    def run(self):
        """
        Run all steps and catch error to notify the user if something goes wrong.

        .. raises:: Exception
        """
        try:
            self._check()
            if self._config.get("database", None):
                self._database()
            self._backup()
            if self._config.get("sync", None):
                self._sync()
            if self._config.get("clean", None):
                self._clean()
        except subprocess.CalledProcessError as e:
            err = "Process fail, command : '{}'".format(" ".join(e.cmd))
            files = {"stdout.log": e.stdout, "stderr.log": e.stderr}
            self.notify(err, attachments=files)
            raise
        except Exception as e:
            self.notify(str(e))
            raise

    def notify(self, msg, attachments={}):
        """
        Fetch notifier driver and send a message to the user.

        :param msg: The message to send
        :param attachments: Dictionary of files to send with the message,
                            with as key the filename and value the file content in bytes.
        :type msg: str
        :type attachments: dict
        """
        configs = self._config.get("notifier", {})

        if isinstance(configs, dict):
            configs = [configs]

        for config in configs:
            driver = notifiers(config.get("driver", "print"))
            notifier = driver(**config)
            notifier.send(msg, attachments)

    def config(self):
        print("Current settings file : '{}'".format(self._cfg_file))

    def add_dir(self, dirs=[]):
        """
        Resolve and add directories path to the config file.
        Also, remove duplicate value.

        :param dirs: Directories to add to the config file
        :type dirs: iterable
        """
        for d in dirs:
            d = Path(d).expanduser().resolve()
            if not d.is_dir():
                raise ValueError("'{}' must be a directory !".format(d))
            cfg_dirs = set(self._config.get("directories", []))
            cfg_dirs.add(str(d))
            self._config["directories"] = list(cfg_dirs)
        self._save_cfg()
