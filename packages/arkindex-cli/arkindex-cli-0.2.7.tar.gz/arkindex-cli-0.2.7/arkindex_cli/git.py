# -*- coding: utf-8 -*-
import logging
import re
import subprocess
from functools import cached_property
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

GIT_SSH_REMOTE = re.compile(r"git@(?P<base>.+):(?P<project>.+)\.git")


class LocalGitRepository(object):
    """
    Helper class to retrieve the attributes of a git project locally
    running commands via sub processes.
    """

    def run(self, *args):
        return subprocess.check_output(args).decode().strip().splitlines()

    @cached_property
    def url(self):
        remote = self.run("git", "remote", "get-url", "origin")
        assert (
            len(remote) == 1
        ), f"Current directory has multiple Git origin URL: {remote}"
        repository_url = remote[0]
        if not repository_url.startswith("http"):
            logger.debug(f"Trying to extract repository URL SSH remote {remote}")
            re_match = GIT_SSH_REMOTE.match(repository_url)
            if not re_match:
                raise ValueError(
                    f"Repository could not be detected from remote {remote}. "
                    "Please ensure you are in a Git project or manually set --repository-url."
                )
            attrs = re_match.groupdict()
            repository_url = urljoin(f"https://{attrs['base']}", attrs["project"])
        return repository_url

    @cached_property
    def hash(self):
        logger.debug("Trying to extract revision hash from the current Git project")
        (revision_hash,) = self.run("git", "rev-parse", "HEAD")
        return revision_hash

    @cached_property
    def message(self):
        logger.debug("Trying to extract revision message from the current Git project")
        return ". ".join(
            self.run("git", "show", "--no-patch", "--format=%B", self.hash)
        )

    @cached_property
    def author(self):
        logger.debug("Trying to extract revision author from the current Git project")
        (author,) = self.run(
            "git", "--no-pager", "show", "--no-patch", "--format=%ae", self.hash
        )
        return author

    @cached_property
    def branch(self):
        logger.debug("Trying to extract revision branch from the current Git project")
        (branch,) = self.run("git", "branch", "--show-current")
        return branch

    @cached_property
    def tags(self):
        logger.debug(
            "Trying to extract a single revision tag from the current Git project"
        )
        return self.run("git", "--no-pager", "tag", "--points-at", self.hash)
