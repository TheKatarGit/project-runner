import requests
import os
from data import Configuration
from loggerconf import logger

# TODO: Implement Logger class
# TODO: Implement Configuration

class Puller(object):
    """Puller class is responsible for pulling data from GitHub.com repos
        via provided repo and branch name."""
    def __init__(self, arg):
        self.__name = arg["name"]
        self.__repo = arg["repo"]
        self.__branch = arg["branch"]
        self.preconfigured_link = Configuration.get_link()

    def check_privileges(self):
        if not os.access(Configuration.get_dir(), os.W_OK):
            logger.error("Application does not have permission to pull repo")
            raise OSError

    def __create_repo_link(self):
        self.__repo_link =  self.preconfigured_link + "/users/" + self.__name + "/repos"

    def __create_branch_link(self):
        self.__branch_link = self.preconfigured_link + "/repos/" + self.__name + "/" + self.__repo + "/branches"

    def get_branch_link(self):
        return self.__branch_link

    def check_data(self):
        self.__create_repo_link()
        self.__data = requests.get(self.__repo_link)
        if self.__data.status_code != 200:
            logger.error("Could not connect to GitHub")
            exit(1)
        try:
            for repo in self.__data.json():
                if repo["name"] == self.__repo:
                    self.__create_branch_link()
                    self.__repo = repo
                    break
            try:
                self.get_branch_link()
            except AttributeError:
                logger.error("Repo was not found. Exiting")
                exit(1)

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

    # TODO: Check possible connectivity errors
    def download_repo(self):
        os.system("git clone {} {}".format(self.__repo["clone_url"], os.path.join(Configuration.get_dir(), "repo")))
        os.system("cd {}".format(os.path.join(Configuration.get_dir(), "repo")))
        os.system("git checkout -b build remotes/origin/{}".format(self.__branch["name"]))
