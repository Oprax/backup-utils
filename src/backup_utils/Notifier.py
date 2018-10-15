from sys import stderr


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
        print(msg, attachments, file=stderr)
