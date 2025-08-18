# from logging import getLogger, basicConfig, DEBUG


# logger = getLogger()
# FORMAT = "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
# basicConfig(level=DEBUG, format=FORMAT)
import logging
from utils import do_something
from com import configure_logging

logger = logging.getLogger(__name__)


def main():
    configure_logging(level=logging.DEBUG)
    logger.warning("Hello! Main start")
    do_something()
    logger.warning("Bye! Finish main")


if __name__ == "__main__":
    main()
