import wx
from time import sleep
from threading import Thread

class LoadingDialog(wx.Dialog):
	def __init__(self, parent, message, func, *args, **kwargs):
		wx.Dialog.__init__(self, parent, title=message)
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.result = ""
		Thread(target=self.run).start()
		self.ShowModal()

	def run(self):
#		try:
		self.result = self.func(*self.args, **self.kwargs)
#		except Exception as e:
#			raise e
		sleep(0.5)
		self.Destroy()
