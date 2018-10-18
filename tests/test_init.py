import sys, json

from pathlib import Path
from unittest.mock import patch

import pytest

from .fixtures import FakeFile


@patch.object(sys, "argv", ["backup_utils", "-v"])
def test_version(capsys):
    from backup_utils import main, __VERSION__

    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert __VERSION__ in captured.out


@patch.object(sys, "argv", ["backup_utils", "-d" "./"])
def test_dir():
    p = str(Path(".").resolve())
    cfg = {}
    with FakeFile("~/.config/bak-utils/config.json") as cfg_file:
        from backup_utils import main

        main()
        cfg.update(json.loads(cfg_file.read_text()))
    assert "directories" in cfg.keys()
    dirs = cfg.get("directories")
    assert len(dirs) == 1
    assert p in dirs
