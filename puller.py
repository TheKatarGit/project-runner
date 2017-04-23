import requests
import os
from loggerconf import logger
from data import PRECONF_LINK

# TODO: Implement Logger class
# TODO: Implement Configuration

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

    def check_data(self):
        __create_repo_link()
        self.__data = requests.get(self.__repo_link)
        if self.__data.status_code != 200:
            logger.error("Could not connect to GitHub")
            exit(1)
        try:
            for repo in self.__data.json():
                if repo["name"] == self.__repo:
                    __create_branch_link()
                    self.__repo = repo
        except ValueError:
            logger.error("GitHub JSON does not contain usual fields. Check GitHub API")
            exit(1)
        self.__branch_list =  requests.get(self.__branch_link)
        if self.__branch_list.status_code != 200:
            logger.error("Could not get repo branches")
            exit(1)
        for branch in self.__branch_list.json():
            if self.__branch == branch["name"]:
                self.__branch = branch
                break

        def download_repo(self):
            # TODO: Check possible connectivity errors
            os.system("git clone {} {}".format(self.__repo["clone_url"], os.path.join(WORKDIR, "repo")))
            os.system("cd {}".format(os.path.join(WORKDIR, "repo")))
            os.system("git checkout -b build /remotes/origin/{}".format(self.__branch["name"]))
