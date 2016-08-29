
from enum import Enum, unique
import logging

@unique
class LEVEL(Enum):
    MAJOR = 0
    MINOR = 1
    MONITOR = 2
    VERBOSE = 3

root_logger = None

class log:

    def __init__(self, level=logging.INFO, use_console=False, log_file="log.log"):
        self.lev = level
        self.use_console = use_console

        global root_logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        _sh = logging.StreamHandler()
        _sh.setLevel(level)
        _sh.setFormatter(formatter)
        root_logger.addHandler(_sh)

        if(log_file is not None):
            _fh = logging.FileHandler(log_file)
            _fh.setLevel(level)
            _fh.setFormatter(formatter)
            root_logger.addHandler(_fh)

    @classmethod
    def log_debug(self, *args):
        global root_logger
        if root_logger is None:
            raise ValueError("logging module need init")
        else:
            root_logger.debug(*args)

    @classmethod
    def log_info(self, *args):
        global root_logger
        if root_logger is None:
            raise ValueError("logging module need init")
        else:
            root_logger.info(*args)

    @classmethod
    def log_warring(self, *args):
        global root_logger
        if root_logger is None:
            raise ValueError("logging module need init")
        else:
            root_logger.warring(*args)

    @classmethod
    def log_error(self, *args):
        global root_logger
        if root_logger is None:
            raise ValueError("logging module need init")
        else:
            root_logger.error(*args)


if __name__ == '__main__':
    try:
        # log(logging.INFO)
        log.log_info("this is a test")
    except ValueError as e:
        print(e)
        raise

    while True:
        try :
            x = int(input("please enter a number: "))
            break
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

