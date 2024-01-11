import logging


def get_logger(name: str):
    '''
    Get full configured logger with pre-build handlers and formatters

    :param name: Name of the logger
    :return: returns full-fledged logger
    '''

    if isinstance(name, str):

        f_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s | %(filename)s/%(funcName)s/%(lineno)d | %(message)s')
        s_formatter = logging.Formatter(
            fmt='%(levelname)s|%(name)s: %(message)s')

        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.DEBUG)
        s_handler.setFormatter(s_formatter)

        f_handler = logging.FileHandler('pylg.log', 'a')
        f_handler.setLevel(logging.WARNING)
        f_handler.setFormatter(f_formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
        logger.addHandler(s_handler)
        logger.addHandler(f_handler)

        return logger

    raise TypeError('Logger name must be string')
