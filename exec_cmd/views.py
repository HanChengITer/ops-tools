from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from exec_cmd.models import ExecCmd, ExecRecord
import json
from django.urls import reverse
from django.shortcuts import redirect
from apis.models import CmdExecuter

# import the logging library
import logging
logger = logging.getLogger('django')

# Create your views here.
def no_suffix(request):
	"""重定向到exec_cmd首页"""
	return HttpResponseRedirect(reverse('exec_cmd:index'))
	
def index(request):
	"""exec_cmd首页"""
	cmds =  ExecCmd.objects.all()
	context = {'cmds': cmds,'is_executed': False}
	return render(request, 'exec_cmd/index.html', context)
	
def execute_selected_cmd(request):
	"""执行选中的历史命令"""
	cmds =  ExecCmd.objects.all()
	context = {'cmds': cmds,'is_executed': True}
	
	params = request.POST.dict()
	
	# 参数校验，可增加校验
	if request.method != 'POST':
		resp = {'detail':'method error, method is not POST'}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	if "selected_cmd" not in params:
		resp = {'detail':'params error, selected_cmd not in params'}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	
	hosts_tmp = None
	cmd_tmp = None
	
	if params["selected_cmd"].startswith("ansible"):
		hosts_tmp, cmd_tmp = params["selected_cmd"][8:].split(' -m shell -a ')
		cmd_tmp = cmd_tmp[1:-1]
	else:
		cmd_tmp = params["selected_cmd"]
	
	logger.info('exec cmd from selected_cmd')
	logger.info(hosts_tmp)
	logger.info(cmd_tmp)
	
	result_dict = CmdExecuter(hosts_tmp, cmd_tmp).execute()
	context["selected_cmd_id"] = ExecCmd.objects.get(hosts=hosts_tmp, cmd=cmd_tmp).id
	context["result"] = result_dict["result"]
		# if result_dict["status"] == "1":
			# resp = {
				# 'status':'error', 
				# 'result':'',
				# 'detail':result_dict["result"],
			# }
			
		# else:
			# resp = {
				# 'status':'success', 
				# 'result':{"des_host":hosts_tmp, "des_cmd":cmd_tmp, "result":result_dict["result"]},
				# 'detail':''
			# }
	
	return render(request, 'exec_cmd/index.html', context)

def create_cmd(request):
	'''新增命令'''
	if request.method != 'GET':
		resp = {'detail':'method error, method is not GET'}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	resp = {'detail':'i have no plan for this method'}
	return HttpResponse(json.dumps(resp), content_type="application/json")

def execute(request):
	"""执行命令"""
	if request.method != 'POST':
		# 
		# resp = {'detail':'get method'}
		# return HttpResponse(json.dumps(resp), content_type="application/json")
		
		context = {"des_host":None, "des_cmd":None, "return_words":None}
		# logger.info('===========' + str(context))
		return render(request, 'exec_cmd/execute.html', context)
		
	else:
		params = request.POST.dict()
		
		
		# 参数校验，可增加校验
		if "des_cmd" not in params:
			resp = {'detail':'params error, des_cmd not in params'}
			return HttpResponse(json.dumps(resp), content_type="application/json")
		
		# 执行命令，获得输出
		des_host = None if "des_host" not in params else params["host"]
		des_cmd = params["des_cmd"]
		return_words = CmdExecuter(des_host, des_cmd).execute()
		
		# resp = {'detail':return_words}
		# return HttpResponse(json.dumps(resp), content_type="application/text")
		
		context = {"des_host":des_host, "des_cmd":des_cmd, "return_words":return_words}
		# logger.info('===========' + str(context))
		return render(request, 'exec_cmd/execute.html', context)
		