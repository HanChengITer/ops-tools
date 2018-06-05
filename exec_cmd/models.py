from django.db import models

# Create your models here.


class ExecCmd(models.Model):
	"""执行的命令"""
	# 执行命令的目标机器
	hosts = models.CharField(max_length=200, null=True, blank=True)
	
	cmd = models.CharField(max_length=200)
	
	date_added = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		if self.hosts != None:
			return 'ansible {} -m shell -a "{}"'.format(self.hosts, self.cmd)
		else:
			return self.cmd

class ExecRecord(models.Model):
	"""执行命令的记录"""
	# 级联外键，删除cmd，则record同步被删除
	cmd = models.ForeignKey(ExecCmd, on_delete=models.CASCADE)
	
	date_executed = models.DateTimeField(auto_now_add=True)
	
	result = models.CharField(max_length=1,choices=(("0","successed"),("1","failed")))
	
	def __str__(self):
		return '**************\nexec time:\n{}\nexec cmd:\n{}\nexec result\n{}**************\n'.format(self.date_executed, self.cmd,self.result)