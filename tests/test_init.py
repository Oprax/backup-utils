import sys
import json

from pathlib import Path
from unittest.mock import patch

import pytest

from conftest import FakeFile, config


@patch.object(sys, "argv", ["backup_utils", "-v"])
def test_version(capsys):
    from backup_utils import main, __version__

    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert __version__ in captured.out


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


# @patch.object(sys, "argv", ["backup_utils", "-r"])
# @patch("backup_utils.databases.databases")
# @patch("backup_utils.syncs.syncs")
# @patch("backup_utils.tasks.tasks")
# def test_run(mock_tasks, mock_syncs, mock_databases, config):
#     cfg = config.copy()
#     cfg.update({"notifier": {"driver": "print"}})
#     with FakeFile(
#         "~/.config/bak-utils/config.json", content=json.dumps(cfg)
#     ) as cfg_file:
#         from backup_utils import main

#         main()
