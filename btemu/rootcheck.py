import logging
import os


class NotRootUser(Exception):
    pass


def rootcheck():
    if not os.geteuid() == 0:
        logging.error("Only root can run this script")
        raise NotRootUser("Only root can run this script")
