from unittest.mock import patch
from subprocess import PIPE

import pytest

from conftest import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    new_cfg.setdefault("sync", {}).update(
        {
            "driver": "rsync",
            "dist": "backup@my.example.org:~/{hostname}",
            "delete": True,
            "excludes": ["test"],
            "ssh_opts": "ssh -p 4242",
        }
    )
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_RsyncSync(mock_which, mock_run, my_cfg):
    from backup_utils.syncs.RsyncSync import RsyncSync
    from backup_utils.utils import render

    t = RsyncSync(repo=my_cfg.get("repo"), **my_cfg.get("sync"))
    t.start()
    mock_run.assert_called_once_with(
        [
            "rsync",
            "-a",
            "--delete",
            "--exclude=test",
            "-e",
            "ssh -p 4242",
            my_cfg.get("repo"),
            render("backup@my.example.org:~/{hostname}"),
        ],
        check=True,
        env=None,
        stderr=PIPE,
        stdout=PIPE,
    )
