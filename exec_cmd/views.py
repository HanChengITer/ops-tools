from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from exec_cmd.models import ExecCmd, ExecRecord
import json,requests
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
	
	# logger.info('exec cmd from selected_cmd')
	# logger.info(hosts_tmp)
	# logger.info(cmd_tmp)
	prefix = 'https://' if request.is_secure() else 'http://'
	new_url = prefix + request.get_host() + reverse('apis:execute')
	# logger.info('path>>>' + new_url)
	if hosts_tmp != None:
		response_dict = dict(requests.post(new_url, data = {'des_host':hosts_tmp, 'des_cmd':cmd_tmp,}).json())
	else:
		response_dict = dict(requests.post(new_url, data = {'des_cmd':cmd_tmp,}).json())
	# logger.info('response_dict>>>' + str(response_dict))
	context["selected_cmd_id"] = response_dict["result"]["executed_cmd_id"]
	context["result"] = response_dict["result"]["result"]
	return render(request, 'exec_cmd/index.html', context)

def create_cmd(request):
	'''新增命令'''
	if request.method != 'GET':
		resp = {'detail':'method error, method is not GET'}
		return HttpResponse(json.dumps(resp), content_type="application/json")
	resp = {'detail':'i have no plan for this method'}
	return HttpResponse(json.dumps(resp), content_type="application/json")
		