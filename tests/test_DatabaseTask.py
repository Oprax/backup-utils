from subprocess import PIPE
from unittest.mock import patch
from pathlib import Path

from conftest import config, utils_which, subprocess_run


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_dbtask(mock_which, mock_run, config):
    from backup_utils.DatabaseTask import DatabaseTask

    t = DatabaseTask(**config.get("database"))
    t.start()
    assert t.backup_dir == config.get("database", {}).get("backup_directory")
    mock_run.assert_any_call("sqldump", check=True, env=None, stderr=PIPE, stdout=PIPE)


def test_dbcompress(config):
    from backup_utils.DatabaseTask import DatabaseTask

    t = DatabaseTask(compression="xz", **config.get("database"))
    p = Path(t.backup_dir) / "dump.sql"
    t.compress(data=b"so much data", fname=str(p))
    bak = Path(t.backup_dir) / "dump.sql.xz"
    assert bak.exists()
    assert bak.read_bytes() == (
        b"\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5"
        b"\xa3\x01\x00\x0bso much data\x00\xf7\x9d\x929:\xa9\xc0\xb1\x00\x01$"
        b"\x0c\xa6\x18\xd8\xd8\x1f\xb6\xf3}\x01\x00\x00\x00\x00\x04YZ"
    )
