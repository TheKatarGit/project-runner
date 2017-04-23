# FIXME: Dead end for now
class Logger(object):
    """Python Logger for Application."""
    def __init__(self):
        self.level = "INFO"

    def error(self, message):
        print(message)

logger = Logger()
