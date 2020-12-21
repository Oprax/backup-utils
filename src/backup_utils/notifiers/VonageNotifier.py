import nexmo

from ..Notifier import Notifier
from ..utils import render


class VonageNotifier(Notifier):
    def send(self, msg, attachments={}):
        """
        .. seealso:: Notifier.send()
        """
        client = nexmo.Client(
            key=self._config.get("vonage_key"), secret=self._config.get("vonage_secret")
        )
        client.send_message(
            {
                "from": render(self._config.get("from", "BackupUtils")),
                "to": self._config.get("to"),
                "text": msg,
            }
        )
