import wx
from scripts.Speak import speak
import re

class ReplaceDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("replace text"))
		p = wx.Panel(self)
		wx.StaticText(p, -1, _("The text to replace"))
		self.firstText = wx.TextCtrl(p, -1)
		wx.StaticText(p, -1, _("replace with"))
		self.secondText =wx.TextCtrl(p, -1)
		self.caseSensitive = wx.CheckBox(p, -1, _("case sensitive letters"))
		replace = wx.Button(p, -1, _("replace text"))
		replaceAll = wx.Button(p, -1, _("replace all"))
		cancel = wx.Button(p, wx.ID_CANCEL, _("cancel"))
		replace.Bind(wx.EVT_BUTTON, self.StartReplace)
		replaceAll.Bind(wx.EVT_BUTTON, lambda e:self.StartReplace(replaceAll=True))
		self.ShowModal()

	def StartReplace(self, event=None, replaceAll=False):
		content = self.Parent.textField.Value if self.caseSensitive.Value else self.Parent.textField.Value.lower()
		first = self.firstText.Value if self.caseSensitive.Value else self.firstText.Value.lower()
		second = self.secondText.Value if self.caseSensitive.Value else self.secondText.Value.lower()
		if not first in content:
			wx.MessageBox(_("The text given to replace was not found."), _("text not found"))
			return
		replaced = re.sub(first, second, content, count=0 if replaceAll else 1)
		self.Parent.textField.Value = replaced
		speak(_("text replaced"))