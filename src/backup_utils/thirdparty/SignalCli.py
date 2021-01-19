import subprocess
import re
import tempfile
from pathlib import Path


REGEX_E164 = re.compile(r"^\+[1-9]\d{1,14}$")


class SignalCli:
    """
    Class wrapper for `signal-cli <https://github.com/AsamK/signal-cli>`_
    """

    def __init__(
        self,
        user=None,
        signal_bin_path="signal-cli",
        signal_config_path=None,
        environment=None,
        debug=False,
    ):
        self._user = user
        self._debug = debug
        self.log = print
        self._env = environment
        self._startup_cmds = [signal_bin_path]

        if signal_config_path is not None:
            signal_config_path = Path(signal_config_path).absolute()
            if not signal_config_path.is_dir():
                raise ValueError(
                    "the given signal configuration path ({}) is not a directory !".format(
                        signal_config_path
                    )
                )
            self._startup_cmds += ["--config", str(signal_config_path)]

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @user.deleter
    def user(self):
        self._user = None

    def _run(self, cmds):
        combine_cmds = self._startup_cmds + cmds
        if self._debug:
            self.log(combine_cmds)
        result = subprocess.run(
            combine_cmds,
            env=self._env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        result.check_returncode()
        return result

    def _check_user(self):
        if not self._user or not REGEX_E164.match(self._user):
            raise ValueError("Given user must be a valid E.164 phone number !")

    def send(self, recipient, message, attachments={}):
        self._check_user()
        if not recipient or not REGEX_E164.match(recipient):
            raise ValueError("Given recipient must be a valid E.164 phone number !")
        result = None
        with tempfile.TemporaryDirectory(prefix="backup-utils-") as tmpdirname:
            cmd = ["-u", self._user, "send", "-m", message, recipient]
            if len(attachments):
                tmpdir = Path(tmpdirname)
                for filename, content in attachments.items():
                    if isinstance(content, str):
                        cmd += ["--attachment", content]
                    elif isinstance(content, bytes):
                        attachment = tmpdir / filename
                        attachment.write_bytes(content)
                        cmd += ["--attachment", str(attachment)]
            result = self._run(cmd)
        return result

    def register(self):
        self._check_user()
        return self._run(["-u", self._user, "register"])

    def verify(self, code):
        self._check_user()
        return self._run(["-u", self._user, "verify", code])

    def receive(self):
        self._check_user()
        return self._run(["-u", self._user, "receive"])

    def link(self, device_name):
        cmd = self._startup_cmds + ["link", "-n", device_name]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        wait_for_output = True
        while wait_for_output:
            output = proc.stdout.readline().strip()
            if len(output):
                wait_for_output = False
                yield output
        return_code = proc.wait()
        if return_code:
            outs, errs = proc.communicate()
            raise subprocess.CalledProcessError(
                return_code, cmd, output=outs, stderr=errs
            )
        yield return_code
