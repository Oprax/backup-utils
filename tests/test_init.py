import sys

from unittest.mock import patch

import pytest


@patch.object(sys, "argv", ["backup_utils", "-v"])
def test_version(capsys):
    from backup_utils import main, __VERSION__

    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert __VERSION__ in captured.out
