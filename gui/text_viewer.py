import wx
import globals as g

class viewer(wx.Dialog):
	def __init__(self, parent, Title, caption, value):
		if not value: return
		wx.Dialog.__init__(self, parent, title=Title)
		p = wx.Panel(self)
		self.Center()
		wx.StaticText(p, -1, caption)
		self.textField = wx.TextCtrl(p, -1, style=wx.TE_MULTILINE+wx.TE_READONLY+wx.HSCROLL)
		self.textField.Value = value
		copy = wx.Button(p, -1, _("copy to clipboard"))
		copy.Bind(wx.EVT_BUTTON, self.OnCopy)
		wx.Button(p, wx.ID_CANCEL, _("close"))
		self.ShowModal()

	def OnCopy(self, event):
		g.copy(str(self.textField.Value))
		wx.MessageBox(_("Text copied to clipboard"), _("success"))