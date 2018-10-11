import subprocess
from os import environ
from .utils import which, render


__all__ = ["Task", "BorgTask", "RcloneTask", "factory"]


class Task(object):
    """
    Parent Task class, if you create a Task, you class must be a children of this class.
    """
    def __init__(self, cmd, **kwargs):
        """
        Create a Task object, take the binary command and multiple other params use as config.

        :param cmd: the command (without arguments), will be pass throug which
        :param kwargs: Other params that will be use for the configuration.
                       Can be very different between each task.
        :type cmd: str
        :type kwargs: dict

        .. seealso:: which()
        """
        self._cmd = which(cmd)
        if not self._cmd:
            raise ValueError("Can't find '{}' binary".format(cmd))
        self._config = kwargs

    def _exec(self, cmds, env=None):
        """
        Method to run a command in the shell and simplify, sortcut of `subprocess.run()`

        :param cmds: Comand and agrument to execute.
        :param env: To override the current environment and to add environment variable.
        :type cmds: iterable
        :type env: dict
        :return: Th result of the command
        :rtype: subprocess.CompletedProcess

        .. seealso:: subprocess.run()
        """
        return subprocess.run(
            cmds, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _hook(self, hook_name):
        """
        Run fetch and run a hook if this one exist.

        :param hook_name: An ID to differentiated each hook.
        :type hook_name: str
        """
        if hook_name in self._config.keys():
            hook = which(self._config[hook_name])
            if not hook:
                raise ValueError(
                    "Can't find '{}' binary for {} hook".format(hook, hook_name)
                )
        self._exec(hook)

    def _run(self):
        """
        Core of the object which will process the Task.

        .. seealso:: start()
        """
        self._exec(self._cmd)

    def start(self):
        """
        Start a task, and lauch hook.
        Prefer this method instead of `_run()`.

        .. seealso:: _run()
        """
        self._hook("pre_hook")
        self._run()
        self._hook("post_hook")


class BorgTask(Task):
    """
    Task to run BorgBackup.

    .. seealso:: Task()
    """
    def _run(self):
        """
        Create a new environment to pass repo path and password to backup.
        Then execute the backup and prune olf backup.
        """
        borg_env = environ.copy()
        borg_env["BORG_PASSPHRASE"] = self._config.get("pswd", "")
        borg_env["BORG_REPO"] = self._config.get("repo")

        compression = self._config.get("compression", "lzma")
        bak_name = render("::{hostname}-{date}")
        borg_cmds = [
            self._cmd,
            "create",
            "-v",
            "--stats",
            "--compression",
            compression,
            "--exclude-caches",
            bak_name,
        ]
        borg_cmds.extend(set(self._config.get("directories", [])))
        self._exec(borg_cmds, env=borg_env)

        prune_cmds = [self._cmd, "prune", "-v", "::"]
        prune_cmds.extend(self._config.get("prune", "-d 7 -w 4 -m 3 -y 1").split(" "))
        self._exec(prune_cmds, env=borg_env)


class RcloneTask(Task):
    """
    Task to synchronize with Rclone.

    .. seealso:: Task()
    """
    def _run(self):
        """
        Synchronize using repo.
        """
        dist = render(self._config.get("dist", ""))
        repo = self._config.get("repo")
        rclone_cmds = [self._cmd, "-v", "sync", repo, dist]
        self._exec(rclone_cmds)


_tasks = {"task": Task, "borg": BorgTask, "rclone": RcloneTask}


def factory(task_name="Task"):
    """
    Return task object depending the name.

    :param task_name: ID of the Task, not case sensitive
    :type task_name: str
    """
    return _tasks[task_name.lower()]
