import pytest

from pathlib import Path

from backup_utils import Backup


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
    cfg.unlink()
    if cfg.exists():
        cfg.unlink()
    cfg_bak.rename(cfg)
