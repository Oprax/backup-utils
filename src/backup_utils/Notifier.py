from smtplib import SMTP
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .utils import hostname, render


class Notifier(object):
    def __init__(self, **kwargs):
        self._config = kwargs

    def send(self, msg, attachments={}):
        print(err, attachments)
        print(msg, attachments)


class EmailNotifier(Notifier):
    def send(self, err, attachments={}):
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
