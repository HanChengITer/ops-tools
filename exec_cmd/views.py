from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import CmdExecuter
import json

# import the logging library
import logging
logger = logging.getLogger('django')

# Create your views here.
def no_suffix(request):
	"""重定向到exec_cmd首页"""
	return HttpResponseRedirect(reverse('exec_cmd:index'))
	
def index(request):
	"""exec_cmd首页"""
	return render(request, 'exec_cmd/index.html')
	
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
		