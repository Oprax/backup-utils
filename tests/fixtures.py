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


class FakeFile:
    def __init__(self, fpath, content=None, charset="utf-8"):
        self._fpath = Path(fpath).expanduser().resolve()
        self._bak = self._fpath.with_suffix(".bak")
        if isinstance(content, str):
            content = content.encode(charset)
        self._content = content

    def __enter__(self):
        self._fpath.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self._bak.exists():
            self._bak.unlink()
        if self._fpath.exists():
            self._bak.touch()
            self._bak.write_bytes(self._fpath.read_bytes())
            self._fpath.unlink()
        if self._content is not None:
            self._fpath.touch(exist_ok=True)
            self._fpath.write_bytes(self._content)
        return self._fpath

    def __exit__(self, *args):
        if self._bak.exists():
            self._fpath.write_bytes(self._bak.read_bytes())
            self._bak.unlink()
        else:
            if self._fpath.exists():
                self._fpath.unlink()


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
