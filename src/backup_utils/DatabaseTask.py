from pathlib import Path
from datetime import date
from gzip import compress

from .Task import Task


class DatabaseTask(Task):
    """
    Parent DatabaseTask class, if you create a DatabaseTask,
    you class must be a children of this class.
    This class is a child of `Task`.

    .. seealso:: Task()
    """

    def start(self):
        """
        Test if the directory to backup database file exist.

        .. seealso:: Task.start()
        """
        self._bak_dir = (
            Path(self._config.get("backup_directory", "")).expanduser().resolve()
        )
        if not self._bak_dir.exists():
            raise ValueError("'{}' directory don't exist !".format(self._bak_dir))
        super().start()

    @property
    def backup_dir(self):
        """
        Return the directory containing database backup.

        :return: Directory containing database backup.
        :rtype: str
        """
        return str(self._bak_dir)


class MysqlTask(DatabaseTask):
    """
    Mysql driver for DatabaseTask.
    """

    def _run(self):
        """
        Create a backup of databe in mysql using mysqldump
        """
        extra_file = (
            Path(self._config.get("extra_file", "~/.my.cnf")).expanduser().resolve()
        )
        if not extra_file.exists():
            raise ValueError("'{}' file don't exist !".format(extra_file))
        now = str(date.today())
        for db in self._config.get("database", []):
            bak_name = "{database}-{date}.sql.gz".format(database=db, date=now)
            bak_file = Path(self.backup_dir) / bak_name
            cmds = [
                self._cmd,
                "--defaults-extra-file={}".format(str(extra_file)),
                "-u",
                self._config.get("user", "root"),
                "--single-transaction",
                "--quick",
                "--lock-tables={}".format(
                    str(self._config.get("lock_tables", False)).lower()
                ),
                db,
            ]
            proc = self._exec(cmds)
            bak_file.write_bytes(compress(proc.stdout))


_tasks = {"database": DatabaseTask, "mysql": MysqlTask}
