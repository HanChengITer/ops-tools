from django.db import models
import os

import logging
logger = logging.getLogger('django')

# Create your models here.
class CmdExecuter():
	def __init__(self, des_host, des_cmd):
		self.__host = des_host
		self.__cmd = des_cmd
	
	def execute(self):
		exec_str = self.__cmd if self.__host == None else "ansible {} -m shell -a \"{}\"".format(self.__host, self.__cmd)
		# logger.info('===========' + exec_str)
		return os.popen(exec_str).read()