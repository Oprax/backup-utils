from ..thirdparty import SignalCli

from ..Notifier import Notifier


class SignalNotifier(Notifier):
    def send(self, msg, attachments={}):
        """
        .. seealso:: Notifier.send()
        """
        signal = SignalCli(user=self._config.get("from"))
        signal.send(self._config.get("to"), msg, attachments=attachments)
