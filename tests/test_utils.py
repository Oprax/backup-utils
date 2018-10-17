import subprocess

import pytest

from .fixtures import directories_setup

from backup_utils import utils


def test_hostname(directories_setup):
    res = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    assert utils.hostname() == res.stdout.decode("utf-8").strip()


def test_which(directories_setup):
    cmd = "ln"
    res = subprocess.run(["which", cmd], stdout=subprocess.PIPE)
    assert utils.which(cmd) == res.stdout.decode("utf-8").strip()
    assert utils.which("not_exist_at_all") is None


def test_render(directories_setup):
    res = subprocess.run(r"date +%Y-%m-%d".split(" "), stdout=subprocess.PIPE)
    today = res.stdout.decode("utf-8").strip()
    res = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = res.stdout.decode("utf-8").strip()
    template = "machine-{hostname}-{date}"
    assert utils.render(template) == template.format(hostname=hostname, date=today)


def test_load(directories_setup):
    from backup_utils.syncs.RcloneSync import RcloneSync
    from backup_utils.notifiers.EmailNotifier import EmailNotifier

    class_ = utils.load("rclone", pkg="backup_utils.syncs", suffix="Sync")
    assert class_ == RcloneSync
    class_ = utils.load("email", pkg="backup_utils.notifiers", suffix="Notifier")
    assert class_ == EmailNotifier
    with pytest.raises(ImportError):
        utils.load("not_exist_at_all", pkg="backup_utils.tasks", suffix="Task")
