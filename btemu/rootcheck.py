import logging
logging.basicConfig(level=logging.DEBUG)

import os
import sys


def rootcheck():
    if not os.geteuid() == 0:
        logging.error("Only root can run this script")
        sys.exit(1)
