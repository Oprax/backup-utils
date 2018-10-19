from unittest.mock import patch
from subprocess import PIPE
from pathlib import Path

import pytest

from ..fixtures import config, utils_which, subprocess_run


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    bk_cfg = new_cfg.get("backup", {})
    bk_cfg.update({"driver": "tar", "name": "{hostname}.tar.xz"})
    del bk_cfg["cmd"]
    del bk_cfg["pre_hook"]
    del bk_cfg["post_hook"]
    new_cfg["backup"] = bk_cfg.copy()
    yield new_cfg


@patch("subprocess.run", side_effect=subprocess_run)
@patch("backup_utils.utils.which", side_effect=utils_which)
def test_TarTask(mock_which, mock_run, my_cfg):
    from backup_utils.tasks.TarTask import TarTask
    from backup_utils.utils import render

    t = TarTask(repo=my_cfg.get("repo"), **my_cfg.get("backup"))
    t.start()
    mock_run.assert_any_call(
        [
            "tar",
            "-c",
            "-J",
            "-f",
            str(Path(my_cfg.get("repo"))/render("{hostname}.tar.xz")),
        ],
        check=True,
        env=None,
        stderr=PIPE,
        stdout=PIPE,
    )
