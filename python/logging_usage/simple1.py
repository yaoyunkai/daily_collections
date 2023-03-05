"""
Logging

Logger
Handler 都是继承自 Filterer


Logger.info
Logger._log
    record = makeRecord -> LogRecord
Logger.handle
    filter
Logger.callHandlers
    Handler.handle
        Handler.filter
        Handler.emit
            Formatter.format message


Create at 2023/3/5 11:57
"""
import logging
import sys

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setStream(sys.stdout)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
