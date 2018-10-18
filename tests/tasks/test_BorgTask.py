from unittest.mock import patch, ANY
from subprocess import PIPE
from os import environ

import pytest

from ..fixtures import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    bk_cfg = new_cfg.get("backup", {})
    bk_cfg.update({"driver": "borg", "pswd": "123456789", "compression": "zlib,3"})
    del bk_cfg["cmd"]
    new_cfg["backup"] = bk_cfg.copy()
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_BorgTask(mock_which, mock_run, my_cfg):
    from backup_utils.tasks.BorgTask import BorgTask
    from backup_utils.utils import render

    test_env = environ.copy()
    test_env["BORG_PASSPHRASE"] = my_cfg.get("backup", {}).get("pswd", "")
    test_env["BORG_REPO"] = my_cfg.get("repo")

    t = BorgTask(repo=my_cfg.get("repo"), **my_cfg.get("backup"))
    t.start()
    mock_run.assert_any_call(
        [
            "borg",
            "create",
            "-v",
            "--stats",
            "--compression",
            my_cfg.get("backup", {}).get("compression", ""),
            "--exclude-caches",
            render("::{hostname}-{date}"),
        ],
        check=True,
        env=ANY,
        stderr=PIPE,
        stdout=PIPE,
    )
    prune_args = ["borg", "prune", "-v", "::"]
    prune_args.extend("-d 7 -w 4 -m 3 -y 1".split(" "))
    mock_run.assert_any_call(prune_args, check=True, env=ANY, stderr=PIPE, stdout=PIPE)
