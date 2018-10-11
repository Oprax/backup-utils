from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .utils import hostname, render


class Notifier(object):
    """
    Parent Notifier class, if you create a Notifier,
    you class must be a children of this class.
    """

    def __init__(self, **kwargs):
        """
        Create a Notifier object,
        take multiple params, as config.

        :param kwargs: Other params that will be use for the configuration.
                       Can be very different between each task.
        :type kwargs: dict
        """
        self._config = kwargs

    def send(self, msg, attachments={}):
        """
        Send the notification, for the base class, just print params.

        :param msg: The message to send
        :param attachments: Dictionary of files to send with the message,
                            with as key the filename and value the file content in byte.
        :type msg: str
        :type attachments: dict
        """
        print(msg, attachments)


class EmailNotifier(Notifier):
    """
    Send an email as Notification, use SMTP protocol.

    .. seealso:: Notifier()
    """

    def send(self, msg, attachments={}):
        """
        .. seealso:: Notifier.send()
        """
        msg = MIMEMultipart()
        subject = render(self._config.get("subject", "Panic"))
        hname = hostname()
        msg["Subject"] = subject
        msg["From"] = self._config.get("from", "backup@" + hname)
        msg["To"] = self._config.get("to", "postmaster@" + hname)

        msg.attach(MIMEText(msg))

        for name, data in attachments.items():
            part = MIMEApplication(data, Name=name)
            part["Content-Disposition"] = 'attachment; filename="{}"'.format(name)
            msg.attach(part)

        s = SMTP(
            self._config.get("host", "smtp." + hname), self._config.get("port", 587)
        )

        s.login(
            self._config.get("login", "postmaster@" + hname),
            self._config.get("pswd", ""),
        )
        s.sendmail(msg["From"], msg["To"], msg.as_string())
        s.quit()


_tasks = {"print": Notifier, "email": EmailNotifier}
