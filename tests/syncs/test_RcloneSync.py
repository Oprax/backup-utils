from unittest.mock import patch
from subprocess import PIPE

import pytest

from ..fixtures import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    new_cfg.setdefault("sync", {}).update(
        {"driver": "rclone", "dist": "s3:backup/{hostname}"}
    )
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_RcloneSync(mock_which, mock_run, my_cfg):
    from backup_utils.syncs.RcloneSync import RcloneSync
    from backup_utils.utils import render

    t = RcloneSync(repo=my_cfg.get("repo"), **my_cfg.get("sync"))
    t.start()
    mock_run.assert_called_once_with(
        ["rclone", "-v", "sync", my_cfg.get("repo"), render("s3:backup/{hostname}")],
        check=True,
        env=None,
        stderr=PIPE,
        stdout=PIPE,
    )
