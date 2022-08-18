"""
contains the class of the extracted emails and links.
"""
import wx
import globals as g
from scripts import web_browser
from scripts.Speak import speak


class ExtractorDialog(wx.Dialog):
	def __init__(self, parent, lst, urls=True):
		if not lst:
			return speak(_("no links found") if urls else _("no emails found"))
		wx.Dialog.__init__(self, parent, title=_("links extractor") if urls else _("emails extractor"))
		self.urls = urls
		p =wx.Panel(self)
		wx.StaticText(p, -1, _("extracted links") if self.urls else _("extracted emails"))
		self.lst=wx.ListBox(p, -1)
		self.lst.Set(lst)
		self.lst.Selection = 0
		copy = wx.Button(p, -1, _("copy to clipboard"))
		copyAll = wx.Button(p, -1, _("copy all to clipboard"))
		copy.Bind(wx.EVT_BUTTON, self.OnCopy)
		copyAll.Bind(wx.EVT_BUTTON, self.OnCopyAll)
		close = wx.Button(p, wx.ID_CANCEL, _("close"))
		self.SetupContext()
		self.lst.Bind(wx.EVT_CHAR_HOOK, self.OnHook)
		self.ShowModal()

	def OnHook(self, event):
		if event.GetKeyCode()==wx.WXK_RETURN:
			web_browser.Open(self.lst.StringSelection if self.urls else f"mailto:{self.lst.StringSelection}")
			speak(_("opening in browser"))
		event.Skip()

	def OnCopy(self, event):
		if self.FindFocus() == self.lst:return
		content = self.lst.StringSelection
		g.copy(content)
		type = "link" if self.urls else "email"
		wx.MessageBox(_("{t} copied to clipboard").format(t=type), _("success"))
		return

	def OnCopyAll(self, event):
		if self.FindFocus() == self.lst:return
		content = "\n".join(self.lst.Strings)
		g.copy(content)
		wx.MessageBox(_("successfully copied to clipboard"), _("success"))

	def SetupContext(self):
		contextMenu = wx.Menu()
		openInBrowser = contextMenu.Append(-1, _("open in browser"))
		copy = contextMenu.Append(-1, _("copy to clipboard"))
		def popup():
			self.PopupMenu(contextMenu)
		self.Bind(wx.EVT_CONTEXT_MENU, lambda e:popup())
		self.Bind(wx.EVT_MENU, self.OnCopy, copy)
		self.Bind(wx.EVT_MENU, lambda e:web_browser.Open(self.lst.StringSelection if self.urls else f"mailto:{self.lst.StringSelection}"), openInBrowser)