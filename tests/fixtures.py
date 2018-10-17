import pytest

from pathlib import Path


def utils_which(args):
    return args


def subprocess_run(cmds, *args, **kwargs):
    from subprocess import CompletedProcess

    return CompletedProcess(cmds, 0, stdout=b"", stderr=b"")


@pytest.yield_fixture()
def config(tmpdir_factory):
    db_dir = tmpdir_factory.mktemp("db")
    repo_dir = tmpdir_factory.mktemp("repo")
    yield {
        "repo": str(repo_dir),
        "backup": {"cmd": "cmd_test", "pre_hook": "hook1", "post_hook": "hook2"},
        "database": {
            "cmd": "sqldump",
            "database": ["myapp", "testapp"],
            "backup_directory": str(db_dir),
        },
    }


@pytest.yield_fixture()
def directories_setup():
    from backup_utils import Backup

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
