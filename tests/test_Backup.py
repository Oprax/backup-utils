from unittest.mock import patch
from pathlib import Path

import pytest

from .fixtures import config


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    new_cfg.update({"notifier": {"driver": "print"}})
    yield new_cfg


def test_notify(my_cfg, capsys):
    from backup_utils import Backup

    b = Backup()
    b._config = my_cfg
    b.notify("testing", {"err.log": b"some data"})
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "testing {'err.log': b'some data'}\n"
