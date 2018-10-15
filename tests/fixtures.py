import pytest

from pathlib import Path

from backup_utils import Backup


_cfg = {"backup": {"cmd": "cmd_test", "pre_hook": "hook1", "post_hook": "hook2"}}


def utils_which(args):
    return args


def subprocess_run(*args, **kwargs):
    from subprocess import CompletedProcess

    cmd = _cfg.get("backup", {}).get("cmd", "cmd_test")
    return CompletedProcess([cmd], 0)


@pytest.yield_fixture()
def config():
    yield _cfg


@pytest.yield_fixture()
def directories_setup():
    cfg = Path(Backup()._cfg_file)
    cfg_bak = cfg.with_suffix(".bak")
    if cfg_bak.exists():
        cfg_bak.unlink()
    cfg.rename(cfg_bak)
    p = Path("./test_directory")
    p.mkdir(mode=0o700, parents=True, exist_ok=True)
    f = Path(p / "file")
    f.write_text("lorem ipsum")
    yield p
    f.unlink()
    p.rmdir()
    if cfg.exists():
        cfg.unlink()
    cfg_bak.rename(cfg)
