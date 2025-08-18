import logging
from random import randint
from time import sleep

logger = logging.getLogger(__name__)


class User:

    def __str__(self):
        sleep(1)
        10000**100000
        return f"{self.__class__.__name__}(id={id(self)})"


def something_expensive():
    sleep(0.5)
    return {"message": "something expensive"}


def do_something():
    word = "qwerty"
    fraction = 1.2345
    number = randint(1, 100)
    user = User()
    logger.debug(
        "Prepare to do smt, number: %s, word = %r, user: %s",
        number,
        word,
        user,
    )
    logger.info(
        "Doing Something, number: %s, word = %r,  %.2f user: %s",
        number,
        word,
        fraction,
        user,
    )
    is_enabled_for_info_level = logger.isEnabledFor(logging.INFO)
    if is_enabled_for_info_level:
        logger.info("Expensive info: %s", something_expensive())
    logger.warning("Done")
