from subprocess import PIPE
from unittest.mock import patch

from .fixtures import config, utils_which, subprocess_run


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_dbtask(mock_which, mock_run, config):
    from backup_utils.DatabaseTask import DatabaseTask

    t = DatabaseTask(**config.get("database"))
    t.start()
    assert t.backup_dir == config.get("database", {}).get("backup_directory")
    mock_run.assert_any_call("sqldump", check=True, env=None, stderr=PIPE, stdout=PIPE)
