import requests
import os
from loggerconf import logger
from data import PRECONF_LINK

class Puller():
    """Puller class is responsible for pulling data from GitHub.com repos
        via provided repo and branch name."""
    def __init__(self, arg):
        self.__name = arg["name"]
        self.__repo = arg["repo"]
        self.__branch = arg["branch"]
        self.preconfigured_link = PRECONF_LINK

    def check_privileges(self):
        if not os.access(PATH, os.W_OK):
            logger.error("Application does not have permission to pull repo")
            raise OSError

    def __create_repo_link(self):
        self.__repo_link =  self.preconfigured_link + "/" + self.__name + "/repos"

    def __create_branch_link(self):
        self.__branch_link = self.preconfigured_link + "/repos/" + self.__name + "/" + self.__repo + "/branches"

    def pull_data(self):
        __create_repo_link()
        self.__data = requests.get(self.__repo_link)
        if self.__data.status_code != 200:
            logger.error("Could not connect to GitHub")
            exit(1)
        try:
            for repo in self.__data.json():
                if repo["name"] == self.__repo:
                    __create_branch_link()
        except ValueError:
            logger.error("GitHub JSON does not contain usual fields. Check GitHub API")
            exit(1)
