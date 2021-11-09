import tempfile
from pathlib import Path
from ..thirdparty import SignalCli
from ..Notifier import Notifier


class SignalNotifier(Notifier):
    def send(self, msg, attachments={}):
        """
        .. seealso:: Notifier.send()
        """
        with tempfile.TemporaryDirectory(prefix="backup-utils-") as tmpdirname:
            tmpdir = Path(tmpdirname)
            attachment_files = []
            for filename, content in attachments.items():
                attachment = tmpdir / filename
                attachment.write_bytes(content)
                attachment_files.append(str(attachment))
            signal = SignalCli(user=self._config.get("from"))
            signal.send(self._config.get("to"), msg, attachments=attachment_files)
