"""
The goal of this project is to create a front to backup program like Borg.
Indeed, Borg is a really great tool for backup,
but I always write a bash script to specify directories I want to save.
I also use Rclone to synchronize my backup to a remote.
And finally I need to backup my database.

There are three steps to backup :
1. Database export
2. Archiving
3. Synchronize

For each step, you can use multiple driver define in the `DatabaseTask.py` or `Task.py`.
Also if something go wrong, all Exceptions are catch to send a notification.

By default, database export use **mysql**, archiving **borg**, and synchronize **rclone**.
"""

import argparse
from .Backup import Backup

__all__ = [Backup.__class__.__name__, "main"]
__VERSION__ = "0.5.5"
__AUTHOR__ = "Oprax <oprax@me.com>"


def main():
    """
    Expose `backup_utils` method as a command line.
    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __VERSION__
    )
    parser.add_argument("-r", "--run", action="store_true", help="Create a new backup")
    parser.add_argument(
        "--test-notifier",
        action="store_true",
        help="Send a notification to test notifier settings",
    )
    parser.add_argument(
        "-d",
        "--dir",
        required=False,
        action="append",
        help="Add a new directory to the backup list, so next run it will be backup",
    )
    args = parser.parse_args()
    bak = Backup()
    if args.dir:
        bak.add_dir(args.dir)
    elif args.test_notifier:
        bak.notify(
            "Hi, your notifier settings is working !",
            attachments={"test.log": b"this is a test"},
        )
    else:
        bak.run()
