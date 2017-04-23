import yaml
import os

class AppConfig(object):
    """Application configurator class."""
    def __init__(self, yamlfile):
        with open(yamlfile, 'r') as yml:
            self.yamlfile = yaml.load(yml)
        try:
            self.__PRECONF_LINK = self.yamlfile["GitAPILink"]
        except KeyError:
            self.__PRECONF_LINK = "https://api.github.com"

        try:
            self.__WORKDIR = self.yamlfile["WorkingDirectory"]
        except KeyError:
            self.__WORKDIR = os.path.abspath("")

    def get_link(self):
        return self.__PRECONF_LINK

    def get_dir(self):
        return self.__WORKDIR
Configuration = AppConfig("config.yml")
