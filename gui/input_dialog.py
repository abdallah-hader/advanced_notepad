"""
class look like wx.GetTextFromUser
"""
import wx

class InputDialog(wx.Dialog):
	def __init__(self, parent, message, caption, multi=False, defaultString=""):
		wx.Dialog.__init__(self, parent, title=message)
		p = wx.Panel(self)
		wx.StaticText(p, -1, caption)
		self.text=wx.TextCtrl(p, -1, style=wx.TE_MULTILINE+wx.HSCROLL if multi else None, value=defaultString if defaultString else None)
		self.result = ""
		ok = wx.Button(p, -1, _("ok"))
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		ok.Bind(wx.EVT_BUTTON, self.OnOk)
		ok.SetDefault()
		self.ShowModal()

	def OnOk(self, event):
		self.result=self.text.Value
		self.Destroy()