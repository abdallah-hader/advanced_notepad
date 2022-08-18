import wx
import sys, os
from language import supported_languages
from scripts.translator import GetLanguages
from scripts.backup import backup
from settingsconfig import *

languages = {index:language for language, index in enumerate(supported_languages.values())}

class SettingsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, id=-1, title=_("program settings"))
		p=wx.Panel(self)
		self.CenterOnParent()
		wx.StaticText(p, -1, _("sections list, choose what you want to modify its settings from the list below"))
		sections=wx.Listbook(p, -1)
		self.general=GeneralSettings(sections)
		self.translate = TranslateSettings(sections)
		backup = BackupSettings(sections)
		sections.AddPage(self.general, _("general settings"))
		sections.AddPage(self.translate, _("Selected text translation settings"))
		sections.AddPage(backup, _("backup and restore"))
		ok = wx.Button(p, -1, _("ok"))
		ok.Bind(wx.EVT_BUTTON, self.OnOk)
		ok.SetDefault()
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		self.ShowModal()

	def OnOk(self, event):
		global languages
		langs = {value:key for key, value in languages.items()}
		lang = self.general.lang.StringSelection
		if not get("cfu") == self.general.cfu.Value:
			new("cfu", self.general.cfu.Value)
		if not get("navigateeffects") == self.general.navigateSounds.Value:
			new("navigateeffects", self.general.navigateSounds.Value)
		if not get("trfrom") == self.translate.From.StringSelection:
			new("trfrom", self.translate.From.StringSelection)
		if not get("trto") == self.translate.to.StringSelection:
			new("trto", self.translate.to.StringSelection)
		if not int(get("getselectedtranslation")) == self.translate.getResult.Selection:
			new("getselectedtranslation", self.translate.getResult.Selection)
		if not self.general.addCopyMark.Selection==int(get("copymark")):
			new("copymark", self.general.addCopyMark.Selection)
		if not self.general.autoSave.Selection==int(get("autosave")):
			new("autosave", self.general.autoSave.Selection)
		if not langs[self.general.lang.Selection] == get("language"):
			new("language", langs[self.general.lang.Selection])
			msg = wx.MessageDialog(self, _("You have changed the program language, and to apply this change you must restart the program, do you want to restart now?"), _("language changed"), style=wx.YES_NO)
			result = msg.ShowModal()
			if result==wx.ID_YES:
				return os.execl(sys.executable, "None")
		self.Destroy()

class GeneralSettings(wx.Panel):
	def __init__(self, parent):
		global languages
		wx.Panel.__init__(self, parent)
		wx.StaticText(self, -1, _("Program language"))
		self.lang = wx.Choice(self, -1)
		wx.StaticText(self, -1, _("Autosave method"))
		self.autoSave=wx.Choice(self, -1, choices=[_("disable"), _("When any letter is written"), _("when space key pressed")])
		wx.StaticText(self, -1, _("Separation mark between add copy"))
		self.addCopyMark = wx.Choice(self, -1, choices=[_("nothing"), _("new line"), _("comma"), _("space")])
		self.cfu = wx.CheckBox(self, -1, _("check for updates on startup"))
		self.navigateSounds = wx.CheckBox(self, -1, _("play sounds when navigate tabs"))
		self.lang.Set(list(supported_languages.keys()))
		try:
			self.lang.Selection = languages[get("language")]
		except KeyError:
			self.lang.Selection = 0
		self.cfu.Value = get("cfu")
		self.addCopyMark.Selection = int(get("copymark"))
		self.autoSave.Selection = int(get("autosave"))
		self.navigateSounds.Value = get("navigateeffects")

class TranslateSettings(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		wx.StaticText(self, -1, _("translate from"))
		self.From = wx.Choice(self, -1)
		wx.StaticText(self, -1, _("translate to"))
		self.to = wx.Choice(self, -1)
		wx.StaticText(self, -1, _("Get the result by"))
		self.getResult=wx.Choice(self, -1, choices=[_("speech only"), _("speech and copy to clipboard"), _("copy to clipboard only")])
		try:
			self.From.Set([lang for lang in GetLanguages()])
			self.From.Insert(_("auto detect"), 0)
			self.to.Set([lang for lang in GetLanguages()])
			try:
				self.to.StringSelection=get("trto")
				self.From.StringSelection=get("trfrom")
				self.getResult.Selection = int(get("getselectedtranslation"))
			except:
				self.to.Selection=0
				self.From.Selection = 0
		except:
			speak(_("An error occurred while trying to get the list of languages"))

class BackupSettings(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		create = wx.Button(self, -1, _("create backup"))
		restore = wx.Button(self, -1, _("restore backup"))
		create.Bind(wx.EVT_BUTTON, lambda e:backup().CreateDataBackup(self.Parent))
		restore.Bind(wx.EVT_BUTTON, lambda e:backup().RestoreBackup(self.Parent))
