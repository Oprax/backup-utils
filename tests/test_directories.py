from pathlib import Path

from fixtures import directories_setup

from backup_utils import Backup


def test_directory(directories_setup):
    d = str(directories_setup)
    fulld = str(Path(d).expanduser().resolve())
    bak = Backup()
    assert fulld not in bak._config.get("directories", [])
    bak.add_dir([d])
    assert fulld in bak._config.get("directories", [])
