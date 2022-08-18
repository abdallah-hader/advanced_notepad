import wx
from . import loading_dialog
from scripts.Speak import speak
from scripts import translator
import globals as g
from settingsconfig import get, new

class TranslateDialog(wx.Dialog):
	def __init__(self, parent):
		if not parent.textField.Value: return speak(_("There is no text to translate."))
		wx.Dialog.__init__(self, parent, title=_("translate text"))
		self.Center()
		p =wx.Panel(self)
		wx.StaticText(p, -1, _("translate from"))
		self.From = wx.Choice(p, -1)
		wx.StaticText(p, -1, _("translate to"))
		self.to = wx.Choice(p, -1)
		self.getText = wx.RadioBox(p, -1, _("How would you like to get the translated text?"), choices=[_("Replace text in the current tab"), _("Put the text in a new tab"), _("copy to clipboard")])
		translate = wx.Button(p, -1, _("start translate"))
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		translate.Bind(wx.EVT_BUTTON, self.OnStart)
		try:
			self.From.Set([lang for lang in translator.GetLanguages()])
			self.From.Insert(_("auto detect"), 0)
			self.to.Set([lang for lang in translator.GetLanguages()])
			try:
				self.From.StringSelection = get("translatefrom") if get("translatefrom") in self.From.Strings else self.From.SetSelection(0)
				self.to.StringSelection = get("translateto") if get("translateto") in self.to.Strings else self.to.SetSelection(0)
			except: pass
		except:
			speak(_("An error occurred while trying to get the list of languages"))
		self.ShowModal()

	def OnStart(self, event):
		result = loading_dialog.LoadingDialog(self, _("The text is being translated, please wait."), translator.translate, self.Parent.textField.Value, self.From.StringSelection if self.From.Selection!=0 else 0, self.to.StringSelection).result
		if not result:
			return wx.MessageBox(_("An error occurred during the translation process, please try again later."), _("error"), style=wx.ICON_ERROR, parent=self)
		r = self.getText.Selection
		if r == 0:
			self.Parent.textField.Value = result
		elif r==1:
			self.Parent.NewFile()
			self.Parent.textField.Value = result
		else:
			g.copy(result)
			self.Parent.textField.Value = result
		wx.MessageBox(_("The text has been translated successfully."), _("success"))
		self.Destroy()
		self.Parent.textField.SetFocus()