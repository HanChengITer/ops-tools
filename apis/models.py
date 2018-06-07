from django.db import models
import os, traceback
import logging
logger = logging.getLogger('django')

from exec_cmd.models import ExecCmd, ExecRecord

# Create your models here.
class CmdExecuter():
	def __init__(self, des_host, des_cmd):
		self.__host = des_host
		self.__cmd = des_cmd
	
	def execute(self):
		exec_cmd_tmp = None
		result_dict = {"status":None, "result":None}
		try:
			exec_str = self.__cmd if self.__host == None else "ansible {} -m shell -a \"{}\"".format(self.__host, self.__cmd)
			# logger.info('===========' + exec_str)
			
			cmd_nums = len(ExecCmd.objects.all().filter(hosts=self.__host, cmd=self.__cmd))
			
			assert cmd_nums in (0,1), "there have more than one same host-cmd data in db"
			
			result = None
			
			if self.__host != None:
				assert os.system("ansible --version")==0, "ansible not install in server"
			
			if cmd_nums == 0:
				exec_cmd_tmp = ExecCmd(hosts=self.__host, cmd=self.__cmd)
				exec_cmd_tmp.save()
			else:
				exec_cmd_tmp = ExecCmd.objects.all().get(hosts=self.__host, cmd=self.__cmd)
			
			result = os.popen(exec_str).read()
			# logger.info(result)
		except:
			result = traceback.format_exc()
			result_dict["status"] = "1"
			ExecRecord(cmd=exec_cmd_tmp, result="1")
		else:
			result_dict["status"] = "0"
			ExecRecord(cmd=exec_cmd_tmp, result="0")
		result_dict["executed_cmd_id"] = exec_cmd_tmp.id
		result_dict["result"] = result
		return result_dict