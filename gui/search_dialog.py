import wx
from scripts.Speak import speak

class SearchDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=-1, title=_("search"))
		p = wx.Panel(self)
		wx.StaticText(p, -1, _("search for?"))
		self.searchWord = wx.TextCtrl(p, -1)
		self.caseSensitive = wx.CheckBox(p, -1, _("case sensitive letters"))
		go = wx.Button(p, -1, _("search"))
		cancel = wx.Button(p, wx.ID_CANCEL, _("cancel"))
		go.SetDefault()
		go.Bind(wx.EVT_BUTTON, self.OnGo)

	def OnGo(self, event):
		string = self.searchWord.Value if self.caseSensitive.Value else self.searchWord.Value.lower()
		if string=="": return
		insertion = self.Parent.textField.GetInsertionPoint()
		content = self.Parent.textField.Value if self.caseSensitive.Value else self.Parent.textField.Value.lower()
		print(content)
		position = content.replace("\n", "\\n").find(string, insertion)
		if position!=-1:
			self.Parent.textField.SetInsertionPoint(position)
			speak(_("Found the next occurrence of text"))
		else:
			wx.MessageBox(_("No search result was found in the text."), _("no result found"))
			return