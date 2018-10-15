from subprocess import PIPE
from unittest.mock import patch

from fixtures import config, utils_which, subprocess_run


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_task(mock_which, mock_run, config):
    from backup_utils.Task import Task

    t = Task(**config.get("backup"))
    t.start()
    mock_run.assert_any_call("hook1", check=True, env=None, stderr=PIPE, stdout=PIPE)
    mock_run.assert_any_call("cmd_test", check=True, env=None, stderr=PIPE, stdout=PIPE)
    mock_run.assert_any_call("hook2", check=True, env=None, stderr=PIPE, stdout=PIPE)
