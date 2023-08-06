import os
import logging
from functools import wraps
from .functool import func_args2kwargs

level_dict = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# 默认的日志格式
datefmt_classic = "%Y-%m-%d %H:%M:%S %z"
fmt_classic = '%(asctime)s %(levelname)s %(name)s: %(message)s'


# 装饰器，自动获取函数的name参数，如果是文件路径，则自动提取文件名作为logger的name
def auto_logger_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs_new = func_args2kwargs(func, *args, **kwargs)
        name = kwargs_new.get("name", "Logger")
        if os.path.exists(name):
            name = os.path.splitext(os.path.basename(name))[0]
        return name

    return wrapper


def getLogger(name="Logger", level=None, isNamePath=True):
    level = logging.INFO if level is None else level
    name = os.path.splitext(os.path.basename(name))[0] if isNamePath else name
    logger = logging.getLogger(name)
    logger.setLevel(level_dict.get(level, logging.DEBUG))
    return logger


def create_stream_logger(name="Logger", log_level=logging.INFO):
    logger = logging.getLogger(name)
    if len(logger.handlers) >= 1:
        logger.handlers.clear()
    formatter = logging.Formatter(fmt=fmt_classic, datefmt=datefmt_classic)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger


def create_file_logger(name, filename, log_level=logging.INFO, with_stream=True):
    logger = logging.getLogger(name)
    if len(logger.handlers) >= 1:
        logger.handlers.clear()
    logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=fmt_classic, datefmt=datefmt_classic)
    handler = logging.FileHandler(filename, mode='a', encoding=None, delay=False)
    handler.setFormatter(formatter)
    if with_stream:
        logger.addHandler(handler)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


# logging.basicConfig(level=logging.INFO,
#                     format=fmt_classic,
#                     datefmt=datefmt_classic)