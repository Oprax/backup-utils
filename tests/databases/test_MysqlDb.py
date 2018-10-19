from unittest.mock import patch
from subprocess import PIPE
from pathlib import Path

import pytest

from ..fixtures import config, utils_which, subprocess_run, FakeFile


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    db_cfg = new_cfg.get("database", {})
    db_cfg.update({"driver": "mysql", "database": ["testing"]})
    del db_cfg["cmd"]
    new_cfg["database"] = db_cfg.copy()
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_MysqlDb(mock_which, mock_run, my_cfg):
    from backup_utils.databases.MysqlDb import MysqlDb

    cnf_content = """[client]
protocol=TCP
host=localhost
user=root
password=root
"""
    with FakeFile("~/.my.cnf", content=cnf_content) as my_cnf:
        t = MysqlDb(repo=my_cfg.get("repo"), **my_cfg.get("database"))
        t.start()
        mock_run.assert_called_once_with(
            [
                "mysqldump",
                "--defaults-extra-file={}".format(my_cnf.expanduser().resolve()),
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
