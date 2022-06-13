# loggers.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler
##########

logfilepath = "./log/"
if os.path.isdir(logfilepath):
    pass
else:
    os.makedirs(logfilepath)
filenames = logfilepath+'logger.log'

logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s') # 要路徑用pathname

# FileHandler
th = TimedRotatingFileHandler(filename=filenames,when='D',interval=1,backupCount=7)
th.setFormatter(formatter)

# StreamerHandler
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(th)
logger.addHandler(sh)