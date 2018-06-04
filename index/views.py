from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def no_suffix(request):
	"""重定向到全局首页"""
	return HttpResponseRedirect(reverse('index:index'))

def index(request):
	"""全局首页"""
	return render(request, 'index/index.html')