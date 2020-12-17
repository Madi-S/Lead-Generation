import logging



def get_logger(name: str):
    if isinstance(name, str):
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s:%(levelno)s | %(filename)s/%(funcName)s/%(lineno)d | %(message)s')

        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.DEBUG)

        f_handler = logging.FileHandler('pylg.log', 'a')
        f_handler.setLevel(logging.WARNING)

        handlers = [s_handler, f_handler]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        for handler in handlers:
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
    raise TypeError('Logger name must be string')