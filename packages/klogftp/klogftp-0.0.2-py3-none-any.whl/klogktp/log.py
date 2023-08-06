import os
import sys
import logging
from pathlib import Path
from datetime import date
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent

class Log_model:
	def __init__(self, getlogger, log_path) -> None:
		self.getlogger = getlogger
		self.__logname = '%s.log' % datetime.strftime(datetime.now(), "%Y-%m-%d")
		self.logdir = log_path
		self.path = log_path + self.__logname
		if not os.path.exists(self.logdir):
			os.mkdir(self.logdir)

	def settings(self, format="%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s"):
		os.makedirs(self.logdir, exist_ok=True)

		logging.basicConfig(
			level=logging.DEBUG,
			format=format,
			filename=self.path
		)
		Log = logging.getLogger(self.getlogger)
		Log.setLevel(logging.DEBUG)

		# 待改
		handler_path = f'{BASE_DIR}/{self.logdir}/{self.__logname}'.replace('\\','').replace('/','')
		handlers = [handler.baseFilename.replace('\\','').replace('/','') for handler in Log.handlers if len(Log.handlers) > 0]

		if handler_path not in handlers:
			fileHandler = logging.FileHandler(self.path, mode="a")
			fileHandler.setLevel(logging.INFO)

			streamHandler = logging.StreamHandler()
			streamHandler.setLevel(logging.WARNING)

			AllFormatter = logging.Formatter(format)
			fileHandler.setFormatter(AllFormatter)
			streamHandler.setFormatter(AllFormatter)

			Log.addHandler(fileHandler)
			Log.addHandler(streamHandler)
		return Log


def logger(message, log_path):
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	LOG_FILENAME = f'{datetime.strftime(datetime.now(), "%Y-%m-%d")}.log'

	logging.basicConfig(
		filename = log_path + LOG_FILENAME,
		level= logging.DEBUG,
		format='%(asctime)s - {username} - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'.format(username = os.environ.get('USERNAME')),
		datefmt='%Y/%m/%d %I:%M:%S'
	)

	logging.debug(message)
	# with open(log_path + LOG_FILENAME, 'a', encoding='utf-8') as file:
	# 	file.read()


def logMessage(level:str ,message:str, log_path:str, **kwargs) -> None:
	if not os.path.exists(log_path):
		os.mkdir(log_path)
	logpath = log_path
	if "logpath" in kwargs:
		logpath = kwargs['logpath']
	if not os.path.exists(logpath):
		os.makedirs(logpath)

	logname = f"{date.today()}.log"
	if "logname" in kwargs:
		logname = kwargs["logname"]

	levelMode = ""
	if level == "debug": levelMode = logging.DEBUG
	elif level == "info": levelMode = logging.INFO
	elif level == "warning": levelMode = logging.WARNING
	elif level == "error": levelMode = logging.ERROR
	elif level == "critical": levelMode = logging.CRITICAL
	elif level == "exception": levelMode = logging.ERROR

	logging.basicConfig(
		filename = os.path.join(logpath, logname),
		level= levelMode,
		format='%(asctime)s - {username} - %(funcName)s - %(levelname)s - %(message)s'.format(username = os.environ.get('USERNAME')),
		datefmt='%Y/%m/%d %I:%M:%S'
	)

	open(os.path.join(logpath, logname), 'a', encoding='utf-8')

	if level == "debug": logging.debug(message)
	elif level == "info": logging.info(message)
	elif level == "warning": logging.warning(message)
	elif level == "error": logging.error(message)
	elif level == "critical": logging.critical(message)
	elif level == "exception": logging.exception(message)