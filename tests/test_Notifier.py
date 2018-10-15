def test_notifier(capsys):
    from backup_utils.Notifier import Notifier

    n = Notifier()
    n.send("testing", {"err.log": b"some data"})
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "testing {'err.log': b'some data'}\n"
