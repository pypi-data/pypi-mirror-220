import time

from remotemanager.logging import LoggingMixin
from remotemanager.storage import SendableMixin

import os

from remotemanager.utils import dir_delta


class TrackedFile(LoggingMixin, SendableMixin):

    __slots__ = ("_remote_path", "_local_path", "_file")

    def __init__(self, local_path, remote_path, file):

        self._remote_path = remote_path
        self._local_path = local_path
        self._file = file

        self._last_seen = {"remote": -1, "local": -1}

    def __repr__(self):
        return self.local

    def __fspath__(self):
        return self.name

    @property
    def name(self):
        return self._file

    @property
    def importstr(self):
        return os.path.splitext(self._file)[0]

    @property
    def remote(self):
        return os.path.join(self._remote_path, self.name)

    @property
    def local(self):
        return os.path.join(self._local_path, self.name)

    @property
    def remote_dir(self):
        return self._remote_path

    @property
    def local_dir(self):
        return self._local_path

    def relative_remote_path(self, other: str) -> str:
        """
        Return a path relative to `cwd`

        Args:
            other:
                working dir to compare against

        Returns:
            relative path
        """
        # if our remote path is an abspath, we already have what we need
        if os.path.isabs(self.remote_dir):
            return self.remote

        # we're already in the remote, just return the filename
        if self.remote_dir == other:
            return self.name

        # find the deepest shared path, treat it as a "root"
        stem = os.path.commonpath([self.remote_dir, other])
        # find how far down this stem is from `other`
        dirdelta = dir_delta(stem, other)
        # generate a ../ string that steps "down" to the common path
        down = "../" * dirdelta

        tmp_remote = self.remote_dir.replace(stem, "").strip("/")
        # rebuild up from our virtual root
        return os.path.join(down, tmp_remote, self.name)

    @property
    def content(self):
        with open(self.local, "r") as o:
            self.confirm_local()
            return o.read()

    def write(self, content: str) -> None:
        """
        Write `content` to the local copy of the file

        Args:
            content:
                content to write
        Returns:
            None
        """
        if not os.path.isdir(self.local_dir):
            os.makedirs(self.local_dir)
        if not os.path.isdir(self.local_dir):
            os.makedirs(self.local_dir)
        with open(self.local, "w+") as o:
            o.write(content)
        self.confirm_local()

    def append(self, content: str) -> None:
        """
        Append `content` to the local copy of the file

        Args:
            content:
                content to append
        Returns:
            None
        """
        if not os.path.isdir(self.local_dir):
            os.makedirs(self.local_dir)
        with open(self.local, "a+") as o:
            o.write(content)
        self.confirm_local()

    def confirm_local(self):
        """
        Confirm sighting of the file locally
        """
        self._last_seen["local"] = int(time.time())

    def confirm_remote(self):
        """
        Confirm sighting of the file on the remote
        """
        self._last_seen["remote"] = int(time.time())

    def last_seen(self, where: str) -> int:
        return self._last_seen[where]

    @property
    def last_seen_local(self):
        return self.last_seen("local")

    @property
    def last_seen_remote(self):
        return self.last_seen("remote")
