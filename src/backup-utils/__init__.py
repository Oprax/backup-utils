import json
import subprocess

from sys import argv
from pathlib import Path

from utils import which


__VERSION__ = '0.1.1'
__AUTHOR__ = 'Oprax <oprax@me.com>'


class Backup():
    def __init__(self):
        self._ROOT = Path(argv[0]).resolve().parent
        self._config = dict()
        self._load_cfg()

    def _load_cfg(self):
        cfg_file = self._ROOT / '.bak-utils.json'
        if not cfg_file.is_file():
            self._save_cfg()
        else:
            self._config = json.loads(cfg_file.read_text())

    def _save_cfg(self):
        cfg_file = self._ROOT / '.bak-utils.json'
        cfg_file.write_text(json.dumps(self._config, indent=4))

    def _check(self):
        borg_cmd = which(self._config.get('BORG_CMD', 'borg'))
        if not borg_cmd:
            raise ValueError("Can't fin borg binary")
        else:
            self._config['BORG_CMD'] = borg_cmd

    def run(self):
        self._check()
        print(self._config['BORG_CMD'])
        print(subprocess.run([self._config['BORG_CMD'], '--version'],
                             check=True,
                             stdout=subprocess.PIPE))

    def add_dir(self, dirs=[]):
        for d in dirs:
            d = Path(d).resolve()
            if not d.is_dir():
                raise ValueError("'{}' must be a directory !".format(d))
            cfg_dirs = self._config.setdefault('directories', [])
            cfg_dirs.append(str(d))
        self._save_cfg()
