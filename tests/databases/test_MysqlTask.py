from unittest.mock import patch
from subprocess import PIPE
from pathlib import Path

import pytest

from ..fixtures import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    new_cfg.setdefault("database", {}).update(
        {"driver": "mysql", "database": ["testing"]}
    )
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_MysqlTask(mock_which, mock_run, my_cfg):
    from backup_utils.databases.MysqlTask import MysqlTask

    t = MysqlTask(repo=my_cfg.get("repo"), **my_cfg.get("database"))
    t.start()
    mock_run.assert_called_once_with(
        [
            "mysqldump",
            "--defaults-extra-file={}".format(Path("~/.my.cnf").expanduser().resolve()),
            "--single-transaction",
            "--quick",
            "--lock-tables=false",
            "testing",
        ],
        check=True,
        env=None,
        stderr=PIPE,
        stdout=PIPE,
    )
