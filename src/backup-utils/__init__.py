import json
import os
import smtplib
import subprocess

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from sys import argv
from datetime import date
from pathlib import Path

from utils import which, hostname


__VERSION__ = "0.2.0"
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
        try:
            subprocess.run(
                cmds,
                env=env,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            err = "Process fail, command : '{}'".format(" ".join(cmds))
            files = {"stdout.log": e.stdout, "stderr.log": e.stderr}
            self.notify(err, attachments=files)
            raise

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

    def _borg(self):
        borg_env = os.environ.copy()
        borg_env["BORG_PASSPHRASE"] = self._config.get("borg", {}).get("pswd", "")
        borg_env["BORG_REPO"] = str(self._repo)

        compression = self._config.get("borg", {}).get("compression", "lzma")
        bak_name = "::{name}-{date}".format(name=hostname(), date=date.today())
        borg_cmds = [
            self._borg_cmd,
            "create",
            "-v",
            "--stats",
            "--compression",
            compression,
            "--exclude-caches",
            bak_name,
        ]
        borg_cmds.extend(set(self._config.get("directories", [])))
        self._run_cmd(borg_cmds, env=borg_env)

        prune_cmds = [self._borg_cmd, "prune", "-v", "::"]
        prune_cmds.extend(
            self._config.get("borg", {}).get(
                "prune", ["-d", "7", "-w", "4", "-m", "3", "-y", "1"]
            )
        )
        self._run_cmd(prune_cmds, env=borg_env)

    def _rclone(self):
        dist = self._config.get("rclone", {}).get("dist", "")
        dist = dist.format(hostname=hostname(), date=date.today())
        rclone_cmds = [self._rclone_cmd, "-v", "sync", self._repo, dist]
        self._run_cmd(rclone_cmds)

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
        Path(self._ROOT / "panic.msg").write_text(msg.as_string())
        s.sendmail(msg["From"], msg["To"], msg.as_string())
        s.quit()

    def run(self):
        self._check()
        self._borg()
        self._rclone()

    def add_dir(self, dirs=[]):
        for d in dirs:
            d = Path(d).expanduser().resolve()
            if not d.is_dir():
                raise ValueError("'{}' must be a directory !".format(d))
            cfg_dirs = set(self._config.setdefault("directories", []))
            cfg_dirs.add(str(d))
            self._config["directories"] = list(cfg_dirs)
        self._save_cfg()
