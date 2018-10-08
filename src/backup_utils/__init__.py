import json
import smtplib
import subprocess

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv
from datetime import date
from pathlib import Path
from gzip import compress

from .Task import BorgTask, RcloneTask
from .utils import which, hostname


__VERSION__ = "0.5.0"
__AUTHOR__ = "Oprax <oprax@me.com>"


class Backup:
    def __init__(self):
        self._ROOT = Path(argv[0]).resolve().parent
        self._config = {}
        self._logs = {}
        self._cfg_file = Path("~/.config/bak-utils/config.json").expanduser()
        self._load_cfg()

    def _load_cfg(self):
        self._cfg_file.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not self._cfg_file.is_file():
            self._save_cfg()
        else:
            self._config = json.loads(self._cfg_file.read_text())

    def _save_cfg(self):
        self._cfg_file.write_text(json.dumps(self._config, indent=4))

    def _run_cmd(self, cmds, env=None):
        return subprocess.run(
            cmds, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _check(self):
        self._repo = Path(self._config.get("repo", ""))
        if not self._repo.is_dir():
            raise ValueError(
                "'{}' is not a directory ! You need to init borg first !".format(
                    self._repo
                )
            )
        self._borg_cmd = which(self._config.get("borg", {}).get("cmd", "borg"))
        if not self._borg_cmd:
            raise ValueError("Can't find borg binary")
        self._rclone_cmd = which(self._config.get("rclone", {}).get("cmd", "rclone"))
        if not self._rclone_cmd:
            raise ValueError("Can't find rclone binary")
        self._mysqldump_cmd = which(
            self._config.get("database", {}).get("cmd", "mysqldump")
        )
        if not self._mysqldump_cmd:
            raise ValueError("Can't find mysqldump binary")

    def _database(self):
        extra_file = (
            Path(self._config.get("database", {}).get("extra_file", "~/.my.cnf"))
            .expanduser()
            .resolve()
        )
        if not extra_file.exists():
            raise ValueError("'{}' file don't exist !".format(extra_file))
        bak_dir = (
            Path(self._config.get("database", {}).get("backup_directory", ""))
            .expanduser()
            .resolve()
        )
        if not bak_dir.exists():
            raise ValueError("'{}' directory don't exist !".format(bak_dir))
        self.add_dir([bak_dir])
        now = str(date.today())
        for db in self._config.get("database", {}).get("database", []):
            bak_name = "{database}-{date}.sql.gz".format(database=db, date=now)
            bak_file = bak_dir / bak_name
            cmds = [
                self._mysqldump_cmd,
                "--defaults-extra-file={}".format(str(extra_file)),
                "-u",
                self._config.get("database", {}).get("user", "root"),
                "--single-transaction",
                "--quick",
                "--lock-tables={}".format(
                    str(
                        self._config.get("database", {}).get("lock_tables", False)
                    ).lower()
                ),
                db,
            ]
            proc = self._run_cmd(cmds)
            bak_file.write_bytes(compress(proc.stdout))

    def _borg(self):
        borg = BorgTask(
            self._config.get("borg", {}).get("cmd", "borg"),
            directories=self._config.get("directories", []),
            repo=str(self._repo),
            **self._config.get("borg", {})
        )
        borg.run()

    def _rclone(self):
        rclone = RcloneTask(
            self._config.get("rclone", {}).get("cmd", "rclone"),
            repo=str(self._repo),
            **self._config.get("rclone", {})
        )
        rclone.run()

    def notify(self, err, attachments={}):
        print(err, attachments)
        msg = MIMEMultipart()
        subject = self._config.get("email", {}).get("subject", "Panic")
        hname = hostname()
        subject = subject.format(hostname=hname, date=date.today())
        msg["Subject"] = subject
        msg["From"] = self._config.get("email", {}).get("from", "backup@" + hname)
        msg["To"] = self._config.get("email", {}).get("to", "postmaster@" + hname)

        msg.attach(MIMEText(err))

        for name, data in attachments.items():
            part = MIMEApplication(data, Name=name)
            part["Content-Disposition"] = 'attachment; filename="{}"'.format(name)
            msg.attach(part)

        s = smtplib.SMTP(
            self._config.get("email", {}).get("host"),
            self._config.get("email", {}).get("port"),
        )

        s.login(
            self._config.get("email", {}).get("login"),
            self._config.get("email", {}).get("pswd"),
        )
        s.sendmail(msg["From"], msg["To"], msg.as_string())
        s.quit()

    def run(self):
        try:
            self._check()
            if self._config.get("database", None):
                self._database()
            self._borg()
            self._rclone()
        except subprocess.CalledProcessError as e:
            err = "Process fail, command : '{}'".format(" ".join(e.cmd))
            files = {"stdout.log": e.stdout, "stderr.log": e.stderr}
            self.notify(err, attachments=files)
            raise
        except Exception as e:
            self.notify(str(e))
            raise

    def add_dir(self, dirs=[]):
        for d in dirs:
            d = Path(d).expanduser().resolve()
            if not d.is_dir():
                raise ValueError("'{}' must be a directory !".format(d))
            cfg_dirs = set(self._config.setdefault("directories", []))
            cfg_dirs.add(str(d))
            self._config["directories"] = list(cfg_dirs)
        self._save_cfg()
