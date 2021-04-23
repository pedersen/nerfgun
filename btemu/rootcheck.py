import os
import sys


def rootcheck():
    if not os.geteuid() == 0:
        sys.exit("Only root can run this script")
