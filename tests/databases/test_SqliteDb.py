from unittest.mock import patch
from subprocess import PIPE
from pathlib import Path

import sqlite3

import pytest

from conftest import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config, tmpdir_factory):
    db_file = Path(str(tmpdir_factory.mktemp("db"))).resolve()
    db_file = db_file / "stocks.db"

    conn = sqlite3.connect(str(db_file))
    c = conn.cursor()

    c.execute(
        """CREATE TABLE stocks
                (date text, trans text, symbol text, qty real, price real)"""
    )
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    conn.commit()
    conn.close()

    new_cfg = config.copy()
    db_cfg = new_cfg.get("database", {})
    db_cfg.update({"driver": "sqlite", "database": [str(db_file)]})
    del db_cfg["cmd"]
    new_cfg["database"] = db_cfg.copy()
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_TarTask(mock_which, mock_run, my_cfg):
    from backup_utils.databases.SqliteDb import SqliteDb

    t = SqliteDb(**my_cfg.get("database"))
    t.start()
    mock_run.assert_called_once_with(
        ["sqlite3", my_cfg.get("database", {}).get("database")[0], ".dump"],
        check=True,
        env=None,
        stderr=PIPE,
        stdout=PIPE,
    )
