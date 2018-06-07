from django.shortcuts import render

from django.http import HttpResponse
import json

from .models import CmdExecuter

# import the logging library
import logging
logger = logging.getLogger('django')

# Create your views here.
def execute(request):
	"""
	执行命令接口
	接受参数
		des_host
		des_cmd
	返回类型
		json
		>>失败
		{
				'status':str, 
				'result':None,
				'detail':str,
			}
		>>成功
		{
				'status':'success', 
				'result':{
					"executed_cmd_id":str, 
					"result":str,
				},
				'detail':None,
			}
	执行举例
		apis/execute?des_host=dg-all:de-all&des_cmd=ls -hlt
	"""
	logger.info('===== apis/execute received a request\n' + str(request.body))
	if request.method != 'POST':
		
		resp = {
			'status':'error', 
			'result':'',
			'detail':'received a "GET" method'
		}
		return HttpResponse(json.dumps(resp, indent=4), content_type="application/json")
		
	else:
		params = request.POST.dict()
		
		# 参数校验，可增加校验
		if "des_cmd" not in params:
			resp = {'detail':'params error, des_cmd not in params'}
			return HttpResponse(json.dumps(resp, indent=4), content_type="application/json")
		
		# 执行命令，获得输出
		des_host = None if "des_host" not in params else params["des_host"]
		des_cmd = params["des_cmd"]
		result_dict = CmdExecuter(des_host, des_cmd).execute()
		
		if result_dict["status"] == "1":
			resp = {
				'status':'error', 
				'result':None,
				'detail':result_dict["result"],
			}
		else:
			resp = {
				'status':'success', 
				'result':{
					"executed_cmd_id":result_dict["executed_cmd_id"], "result":result_dict["result"],
				},
				'detail':None,
			}
		return HttpResponse(json.dumps(resp, indent=4), content_type="application/json")