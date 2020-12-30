import requests

from ..Notifier import Notifier


class SlackNotifier(Notifier):
    def send(self, msg, attachments={}):
        """
        .. seealso:: Notifier.send()
        """
        blocks = [
            {
                "type": "section",
                "text": {"type": "plain_text", "text": msg},
            },
        ]

        for filename, content in attachments.items():
            blocks.append({"type": "divider"})
            blocks.append(
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": filename},
                }
            )
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "```{}```".format(
                            content.decode("utf-8", errors="replace")
                        ),
                    },
                }
            )
        requests.post(
            self._config.get("webhook_url"),
            json={"blocks": blocks},
        )
