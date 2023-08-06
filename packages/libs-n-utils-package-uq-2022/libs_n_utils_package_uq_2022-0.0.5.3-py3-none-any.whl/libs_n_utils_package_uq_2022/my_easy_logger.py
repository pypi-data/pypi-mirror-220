"""
This lib provides facilities for easy logging as shown by examples here

"""

import logging
import inspect
import colorlog
import os
import datetime
from functools import wraps


def my_logger(reporter_file_name=None, reporter_func_name=None, log_level=None, log_file_address=None, **color_spec):
    debug_c, info_c, warn_c, error_c, critic_c = ['cyan', 'blue,bg_white', 'yellow', 'red', 'red,bg_white']
    if 'debug_c' in color_spec.keys():
        debug_c = color_spec['debug_c']
    if 'info_c' in color_spec.keys():
        info_c = color_spec['info_c']
    if 'warn_c' in color_spec.keys():
        warn_c = color_spec['warn_c']
    if 'error_c' in color_spec.keys():
        error_c = color_spec['error_c']
    if 'critic_c' in color_spec.keys():
        critic_c = color_spec['critic_c']

    if reporter_file_name is None:
        frame = inspect.currentframe()
        frame = frame.f_back
        code = frame.f_code
        reporter_file_name = code.co_filename
        reporter_file_name = reporter_file_name.split('/')[-1]
        # reporter_file_name = os.path.split(__file__)[1]

    if reporter_func_name is None:
        reporter_func_name = '__main__'
    logger_ = logging.getLogger(f'{reporter_file_name}.{reporter_func_name}')
    while len(logger_.handlers) > 0:
        logger_.removeHandler(logger_.handlers[0])
    colH = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(fmt='%(log_color)s%(asctime)s-[%(name)s:%(lineno)d]: %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S',
                                          log_colors={'DEBUG': debug_c,
                                                      'INFO': info_c,
                                                      'WARNING': warn_c,
                                                      'ERROR': error_c,
                                                      'CRITICAL': critic_c})
    colH.setFormatter(formatter)
    logger_.addHandler(colH)
    if log_level is None:
        log_level = logging.INFO
    else:
        log_level = log_level.upper()
        log_level = eval(f'logging.{log_level}')

    logger_.setLevel(log_level)

    if log_file_address is not None:
        fH = logging.FileHandler(log_file_address)
        logger_.addHandler(fH)

    return logger_


def logger_cleaner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logger' not in kwargs:
            logger_ = my_logger(
                reporter_func_name=__name__,
                info_c='black,bg_white'
            )
            script_name = func.__code__.co_filename.split('/')[-1][:-3]
            func_name = func.__name__
            this_logger_name = script_name + "." + func_name
            logger_.name = this_logger_name
            kwargs['logger'] = logger_
        else:
            logger_ = kwargs['logger']

        logger_name = logger_.name
        log_level = logger_.level
        logger_info_color = logger_.handlers[0].formatter.log_colors['INFO']
        outputs = func(*args, **kwargs)
        logger_.name = logger_name
        logger_.handlers[0].formatter.log_colors['INFO'] = logger_info_color
        logger_.setLevel(log_level)
        return outputs

    return wrapper


# ########################################### test functions #########################################################
def _test_func1():
    func_name = inspect.stack()[0][3]
    logger = my_logger(reporter_file_name=inspect.stack()[0][3], reporter_func_name=func_name)
    logger.info(f'Logging from {func_name}')
    pass


def _test_func2():
    func_name = inspect.stack()[0][3]
    logger = my_logger(reporter_func_name=func_name, info_c='yellow,bg_green')
    logger.info(f'Logging from {func_name}')
    pass


# ########################################### test functions ##########################################################


if __name__ == '__main__':
    filename = os.path.split(__file__)[1]
    fldr = r'D:\Python_Project\siamak\domain_cuda\outputs\logs'
    log_file = os.path.join(fldr, f'{filename[:-3]}-{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")}')
    logger = my_logger(reporter_func_name=__name__, info_c='yellow,bg_red', log_file_address=log_file)
    logger.info(f'Logging from {__name__}')
    logger.error('ERRORRRRRRRR')
    logger.critical('CRITICALLLLLLLLLLLLLLL')
    _test_func1()
    _test_func2()
