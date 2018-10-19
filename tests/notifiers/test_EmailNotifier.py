from unittest.mock import patch, ANY, call
import pytest
from ..fixtures import config


@pytest.yield_fixture()
def my_cfg(config):
    new_cfg = config.copy()
    new_cfg.setdefault("notifier", {}).update(
        {
            "driver": "email",
            "subject": "Panic",
            "from": "backup@mg.example.org",
            "to": "postmaster@mg.example.org",
            "host": "smtp.mailgun.org",
            "port": 587,
            "login": "postmaster@mg.example.org",
            "pswd": "p455w0rd",
        }
    )
    yield new_cfg


@patch("backup_utils.notifiers.EmailNotifier.SMTP")
def test_email(mock_SMTP, my_cfg):
    from backup_utils.notifiers.EmailNotifier import EmailNotifier

    cfg = dict(**my_cfg.get("notifier"))
    t = EmailNotifier(**cfg)
    t.send("testing email", {"testing.log": b"random data"})
    assert mock_SMTP.mock_calls == [
        call(cfg.get("host"), cfg.get("port")),
        call().login(cfg.get("login"), cfg.get("pswd")),
        call().sendmail(cfg.get("from"), cfg.get("to"), ANY),
        call().quit(),
    ]
