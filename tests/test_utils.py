import subprocess

import pytest


def test_hostname():
    from backup_utils.utils import hostname

    res = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    assert hostname() == res.stdout.decode("utf-8").strip()


def test_which():
    from backup_utils.utils import which

    cmd = "ln"
    res = subprocess.run(["which", cmd], stdout=subprocess.PIPE)
    assert which(cmd) == res.stdout.decode("utf-8").strip()
    assert which("not_exist_at_all") is None


def test_render():
    from backup_utils.utils import render

    res = subprocess.run(r"date +%Y-%m-%d".split(" "), stdout=subprocess.PIPE)
    today = res.stdout.decode("utf-8").strip()
    res = subprocess.run(["hostname"], stdout=subprocess.PIPE)
    hostname = res.stdout.decode("utf-8").strip()
    template = "machine-{hostname}-{date}"
    assert render(template) == template.format(hostname=hostname, date=today)


def test_load():
    from backup_utils.utils import load
    from backup_utils.syncs.RcloneSync import RcloneSync
    from backup_utils.notifiers.EmailNotifier import EmailNotifier

    class_ = load("rclone", pkg="backup_utils.syncs", suffix="Sync")
    assert class_ == RcloneSync
    class_ = load("email", pkg="backup_utils.notifiers", suffix="Notifier")
    assert class_ == EmailNotifier
    with pytest.raises(ImportError):
        load("not_exist_at_all", pkg="backup_utils.tasks", suffix="Task")
