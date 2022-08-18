# import the important modules and scripts
import os
os.chdir	(os.path.abspath(os.path.dirname(__file__)))
os.add_dll_directory(os.getcwd())
import wx
import globals as g
import shelve
import application
import sys
from language import init_translation
from settingsconfig import get, new, init_config, datapath
from scripts import editor, backup, finder
from scripts.translator import TranslateSelection, SwitchLangs
from docs_handler import GetDoc
from scripts.Speak import speak
from scripts.web_browser import Open
from gui import search_dialog, replace_dialog, text_viewer, extractor_dialog, translate_dialog, settings_dialog
from gui.updater import cfu
from html_handler import html_handler
from threading import Thread

init_translation("AdvancedNotepad") #initialize the translation with the domain
init_config() #initializing the configuration of the program

class notepad(wx.Frame): # the main class
	def __init__(self, file=None):
		g.appInfo = application.info()
		wx.Frame.__init__(self, parent=None, title=g.appInfo.name)
		g.UpdateTabs() # get the tabs from data and save it in to variable in the globals
		p=wx.Panel(self)
		self.Center()
		self.html = html_handler
		self.textField = editor.TextBox(p, -1)
		self.MenuBarSetup() #execute the function of Menu Bar creation
		self.Bind(wx.EVT_CLOSE, self.OnExit)
		for i in p.GetChildren():
			i.Bind(wx.EVT_KEY_DOWN, self.shortcuts)

		if file:
			self.textField.load_file(file)
		else:
			self.LoadLastTab()
		Thread(target=cfu, args=[True]).start() if get("cfu") else None
		self.Show()

	def MenuBarSetup(self):
		menubar = wx.MenuBar()
#define the menus
		file = wx.Menu()
		edit = wx.Menu()
		tools = wx.Menu()
		about = wx.Menu()
		htmlMenu = wx.Menu()
		contactMenu = wx.Menu()
		extractMenu = wx.Menu()
		translateMenu = wx.Menu()
		menubar.Append(file, _("file"))
		menubar.Append(edit, _("edit"))
		menubar.Append(tools, _("tools"))
		menubar.Append(htmlMenu, _("html"))
		menubar.Append(about, _("about"))
#the file menu options
		new = file.Append(-1, _("new: ctrl+n"))
		NewWindow = file.Append(-1, _("new window: ctrl+shift+n"))
		open = file.Append(-1, _("open file: ctrl+o"))
		save = file.Append(-1, _("save: ctrl+s"))
		saveAs = file.Append(-1, _("save as: ctrl+shift+s"))
		checkForUpdates = file.Append(-1, _("check for updates"))
		settings = file.Append(-1, _("settings: alt+s"))
		exit = file.Append(-1, _("exit"))
#edit menu options
		undo = edit.Append(-1, _("UnDo: ctrl+z"))
		cut = edit.Append(-1, _("cut: ctrl+x"))
		copy = edit.Append(-1, _("copy: ctrl+c"))
		paste = edit.Append(-1, _("paste: ctrl+v"))
		addCopy = edit.Append(-1, _("add copy: ctrl+d"))
		insertTime = edit.Append(-1, _("insert date and time: f5"))
		search = edit.Append(-1, _("Find: ctrl+f"))
		replace = edit.Append(-1, _("replace text: ctrl+h"))
		goTo = edit.Append(-1, _("go to: ctrl+g"))
#tools menu options
		translate = tools.AppendSubMenu(translateMenu, _("translate"))
		extract = tools.AppendSubMenu(extractMenu, _("extract"))
		urls = extractMenu.Append(-1, _("links: ctrl+u"))
		emails = extractMenu.Append(-1, _("emails: ctrl+e"))
		translateSelection = translateMenu.Append(-1, _("translate the selected text: ctrl+t"))
		translateAll = translateMenu.Append(-1, _("Translate the entire file: ctrl+shift+t"))
#the about menu options
		aboutTheProgram = about.Append(-1, _("about"))
		help = about.Append(-1, _("help file: f1"))
		telegramChannel = about.Append(-1, _("telegram channel"))
		contact = about.AppendSubMenu(contactMenu, _("contact us"))
		telegram = contactMenu.Append(-1, "telegram")
		facebook = contactMenu.Append(-1, "facebook")
		twitter = contactMenu.Append(-1, "twitter")
#html menu.
		heading = htmlMenu.Append(-1, _("create heading: alt+h"))
		url = htmlMenu.Append(-1, _("create URL: alt+u"))
		lst= htmlMenu.Append(-1, _("create list: alt+l"))
		paragraph = htmlMenu.Append(-1, _("create paragraph: alt+p"))
#binding the options
#the file menu
		self.Bind(wx.EVT_MENU, self.OnOpen, open)
		self.Bind(wx.EVT_MENU, self.save, save)
		self.Bind(wx.EVT_MENU, self.NewFile, new)
		self.Bind(wx.EVT_MENU, lambda e:os.startfile(sys.executable), NewWindow)
		self.Bind(wx.EVT_MENU, self.OnExit, exit)
		self.Bind(wx.EVT_MENU, lambda e:self.save(saveAs=True), saveAs)
		self.Bind(wx.EVT_MENU, lambda e:settings_dialog.SettingsDialog(self), settings)
		self.Bind(wx.EVT_MENU, lambda e:cfu(), checkForUpdates)
#the edit menu
		self.Bind(wx.EVT_MENU, lambda e:g.AddCopy(self.textField.StringSelection), addCopy)
		self.Bind(wx.EVT_MENU, lambda e:replace_dialog.ReplaceDialog(self), replace)
		self.Bind(wx.EVT_MENU, self.GoTo, goTo)
		self.Bind(wx.EVT_MENU, self.OnSearch, search)
		self.Bind(wx.EVT_MENU, self.textField.WriteTime, insertTime)
		self.Bind(wx.EVT_MENU, lambda e:self.textField.Undo(), undo)
		self.Bind(wx.EVT_MENU, lambda e:self.textField.Paste(), paste)
		self.Bind(wx.EVT_MENU, lambda e:self.textField.Copy(), copy)
		self.Bind(wx.EVT_MENU, lambda e:self.textField.Cut(), cut)
# the tools menu
		self.Bind(wx.EVT_MENU, lambda e: extractor_dialog.ExtractorDialog(self, finder.FindUrls(self.textField.Value)), urls)
		self.Bind(wx.EVT_MENU, lambda e:extractor_dialog.ExtractorDialog(self, finder.FindEmails(self.textField.Value), False), emails)
		self.Bind(wx.EVT_MENU, lambda e:translate_dialog.TranslateDialog(self), translateAll)
		self.Bind(wx.EVT_MENU, lambda e:TranslateSelection(self.textField.StringSelection), translateSelection)
#about items
		self.Bind(wx.EVT_MENU, lambda e:wx.MessageBox(g.appInfo.about, _("about the program")), aboutTheProgram)
		self.Bind(wx.EVT_MENU, lambda e:Open(g.appInfo.telegram), telegram)
		self.Bind(wx.EVT_MENU, lambda e:Open(g.appInfo.twitter), twitter)
		self.Bind(wx.EVT_MENU, lambda e:Open(g.appInfo.facebook), facebook)
		self.Bind(wx.EVT_MENU, lambda e:Open(g.appInfo.tchannel), telegramChannel)
		self.Bind(wx.EVT_MENU, lambda e:text_viewer.viewer(self, _("help"), _("help"), GetDoc()), help)
#html items
		self.Bind(wx.EVT_MENU, lambda e:self.html.HeadingsDialog(self), heading)
		self.Bind(wx.EVT_MENU, lambda e:self.html.UrlsDialog(self), url)
		self.Bind(wx.EVT_MENU, lambda e:self.html.ParagraphsDialog(self), paragraph)
		self.Bind(wx.EVT_MENU, lambda e:self.html.ListsDialog(self), lst)
		shortcuts = wx.AcceleratorTable([
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("N"), NewWindow.GetId()),
			(wx.ACCEL_CTRL, ord("N"), new.GetId()),
			(wx.ACCEL_CTRL, ord("O"), open.GetId()),
			(wx.ACCEL_CTRL, ord("S"), save.GetId()),
			(wx.ACCEL_CTRL, ord("G"), goTo.GetId()),
			(wx.ACCEL_CTRL, ord("F"), search.GetId()),
			(wx.ACCEL_CTRL, ord("H"), replace.GetId()),
			(wx.ACCEL_CTRL, ord("U"), urls.GetId()),
			(wx.ACCEL_CTRL, ord("E"), emails.GetId()),
			(wx.ACCEL_CTRL+wx.ACCEL_SHIFT, ord("T"), translateAll.GetId()),
			(wx.ACCEL_ALT, ord("S"), settings.GetId()),
			(wx.ACCEL_CTRL, ord("T"), translateSelection.GetId()),
			(wx.ACCEL_CTRL, ord("D"), addCopy.GetId()),
			(wx.ACCEL_ALT, ord("H"), heading.GetId()),
			(wx.ACCEL_ALT, ord("U"), url.GetId()),
			(wx.ACCEL_ALT, ord("P"), paragraph.GetId()),
			(wx.ACCEL_ALT, ord("L"), lst.GetId()),
			(0, wx.WXK_F1, help.GetId()),
		])
		self.SetAcceleratorTable(shortcuts)
		self.SetMenuBar(menubar)

	def NewFile(self, event=None):
		return self.textField.NewTab()

	def LoadLastTab(self):
		try:
			with shelve.open(os.path.join(datapath, "backup")) as f:
				file = f["last"]
				if not file in g.tabs: return
				self.textField.load_file(file)
		except: pass

	def GoTo(self, event=None):
		position = self.textField.PositionToXY(self.textField.InsertionPoint)
		lineNumber = wx.GetNumberFromUser(_("line number"), _("line number"), _("go to line"), position[-1], min=0, max=self.textField.NumberOfLines, parent=self)
		self.textField.InsertionPoint = self.textField.XYToPosition(1, lineNumber)

	def OnSearch(self, event=None):
		search = search_dialog.SearchDialog(self)
		search.ShowModal()

	def OnOpen(self, event):
		path = wx.FileSelector(_("open file"), wildcard=_("all files(*.*)|*.*|text documents(.txt)|*.txt|python scripts(.py)|*.py|html page(.html)|*.html"), parent = self)
		if not path: return
		g.activeFile = path
		self.textField.load_file(path)
#		self.TabsSetup()

	def save(self, event=None, saveAs=False):
		self.textField.OnWrite(None)
		if not g.activeFile == None and not saveAs:
			saveFile = g.activeFile
		else:
			saveFile = wx.SaveFileSelector(_("Save As"), _("text documents(.txt)|*.txt|python scripts(.py)|*.py|html page(.html)|*.html"), parent=self)
			if not saveFile: return
			if os.path.isfile(saveFile):
				msg = wx.MessageBox(_("The file {f} already exists, do you want to replace it?").format(f=saveFile), _("file exists"), style=wx.YES_NO, parent=self)
				if msg==wx.NO:
					return
		with open(saveFile, "w",encoding="utf-8") as file:
			file.write(self.textField.Value)
			self.textField.modified = False
		g.activeFile = saveFile
		if g.newTab:
			backup.backup().delete(g.paths[g.tabIndex])
		speak(_("File saved successfully"))
		self.textField.load_file(g.activeFile)

	def OnExit(self, event=None):
		self.textField.SavePosition()
		if self.textField.modified:
			dialog = wx.MessageDialog(self, _("Do you want to save changes to Untitled?"), g.appInfo.name, style=wx.YES_NO+wx.CANCEL)
			dialog.SetYesNoCancelLabels(_("&save"), _("&dont save"), _("&cancel"))
			result = dialog.ShowModal()
			if result ==wx.ID_YES:
				self.save()
			elif result == wx.ID_NO:
				return wx.Exit()
			elif result == wx.ID_CANCEL: return
		else: return wx.Exit()

	def FirstTab(self):
		if len(g.paths)<1: return speak(_("there is no tabs"))
		if g.tabIndex==0: return speak(_("the focus already on the first tab"))
		g.tabIndex = 0
		self.textField.load_file(g.tabs[g.paths[g.tabIndex]]["path"])
		if not g.activeFile==None:
			fn = os.path.basename(g.activeFile)
		else:
			try:
				fn = os.path.basename(g.paths[g.tabIndex])
			except:
				fn = g.paths[g.tabIndex]
		g.playsound("previous_tab.wav") if get("navigateeffects") else None
		speak(_("{fileName} {path} {firstNumber} of {secondNumber}").format(fileName=fn, firstNumber=g.tabIndex+1, secondNumber=len(g.paths), path="- "+g.paths[g.tabIndex]+"," if not g.tabs[g.paths[g.tabIndex]]["newTab"] else ""))

	def LastTab(self):
		if len(g.tabs)<1: return speak(_("there is no tabs"))
		if g.tabIndex==len(g.paths)-1: return speak(_("the focus already on the last tab"))
		g.tabIndex = len(g.paths)-1
		self.textField.load_file(g.tabs[g.paths[g.tabIndex]]["path"])
		if not g.activeFile==None:
			fn = os.path.basename(g.activeFile)
		else:
			try:
				fn = os.path.basename(g.paths[g.tabIndex])
			except:
				fn = g.paths[g.tabIndex]
		g.playsound("next_tab.wav") if get("navigateeffects") else None
		speak(_("{fileName} {path} {firstNumber} of {secondNumber}").format(fileName=fn, firstNumber=g.tabIndex+1, secondNumber=len(g.paths), path="- "+g.paths[g.tabIndex]+"," if not g.tabs[g.paths[g.tabIndex]]["newTab"] else ""))

	def NextTab(self):
		if len(g.tabs)<1: return speak(_("there is no tabs"))
#		self.textField.SavePosition()
		if g.tabIndex>=len(g.paths)-1:
			g.tabIndex = 0
		else:
			g.tabIndex+=1
		self.textField.load_file(g.tabs[g.paths[g.tabIndex]]["path"])
		if not g.activeFile==None:
			fn = os.path.basename(g.activeFile)
		else:
			try:
				fn = os.path.basename(g.paths[g.tabIndex])
			except:
				fn = g.paths[g.tabIndex]
		g.playsound("next_tab.wav") if get("navigateeffects") else None
		speak(_("{fileName} {path} {firstNumber} of {secondNumber}").format(fileName=fn, firstNumber=g.tabIndex+1, secondNumber=len(g.paths), path="- "+g.paths[g.tabIndex]+"," if not g.tabs[g.paths[g.tabIndex]]["newTab"] else ""))

	def PreviousTab(self):
		if len(g.tabs)<1: return speak(_("there is no tabs"))
#		self.textField.SavePosition()
		if g.tabIndex<=0:
			g.tabIndex = len(g.tabs)-1
		else:
			g.tabIndex-=1
		self.textField.load_file(g.tabs[g.paths[g.tabIndex]]["path"])
		if not g.activeFile==None:
			fn = os.path.basename(g.activeFile)
		else:

			try:
				fn = os.path.basename(g.paths[g.tabIndex])
			except:
				fn = g.paths[g.tabIndex]
		g.playsound("previous_tab.wav") if get("navigateeffects") else None
		speak(_("{fileName} {path} {firstNumber} of {secondNumber}").format(fileName=fn, firstNumber=g.tabIndex+1, secondNumber=len(g.paths), path="- "+g.paths[g.tabIndex]+"," if not g.tabs[g.paths[g.tabIndex]]["newTab"] else ""))

	def RestoreText(self):
		if g.activeFile is None: return speak(_("current active is unsaved tab"))
		try:
			with open(g.activeFile, "r", encoding="utf-8") as f:
				self.textField.Value=f.read()
		except:
			with open(g.activeFile, "r", encoding="ansi") as f:
				self.textField.Value=f.read()
		self.textField.modified = False
		speak(_("text restored"))


	def CloseTab(self):
		if g.activeFile==None and not g.newTab: return speak(_("select a tab first"))
		if g.activeFile==None:
			if not self.textField.Value:
				backup.backup().delete(g.paths[g.tabIndex])
				speak(_("tab closed"))
				self.textField.clear()
				return self.NextTab()
			dialog = wx.MessageDialog(self, _("If you close the tab, you can't get it back, do you want to save to a file?"), g.appInfo.name, style=wx.YES_NO+wx.CANCEL)
			dialog.SetYesNoCancelLabels(_("&save"), _("&dont save"), _("&cancel"))
			result = dialog.ShowModal()
			if result ==wx.ID_YES:
				self.save()
				backup.backup().delete(g.paths[g.tabIndex])
				speak(_("tab closed"))
				self.textField.clear()
				return self.NextTab()
			elif result == wx.ID_NO:
				backup.backup().delete(g.paths[g.tabIndex])
				speak(_("tab closed"))
				self.textField.clear()
				return self.NextTab()
			else: return
		else:
			try:
				with open(g.activeFile, "r", encoding="utf-8") as f:
					content = f.read()
			except:
				with open(g.activeFile, "r", encoding="ansi") as f:
					content = f.read()
			if content==self.textField.Value:
				backup.backup().delete(g.paths[g.tabIndex])
				speak(_("tab closed"))
				self.textField.clear()
				return self.NextTab()
			else:
				dialog = wx.MessageDialog(self, _("If you close the tab, you can't get it back, do you want to save changes?"), g.appInfo.name, style=wx.YES_NO+wx.CANCEL)
				dialog.SetYesNoCancelLabels(_("&save"), _("&dont save"), _("&cancel"))
				result = dialog.ShowModal()
				if result ==wx.ID_YES:
					self.save()
					backup.backup().delete(g.paths[g.tabIndex])
					speak(_("tab closed"))
					self.textField.clear()
					return self.NextTab()
				elif result == wx.ID_NO:
					backup.backup().delete(g.paths[g.tabIndex])
					speak(_("tab closed"))
					self.textField.clear()
					return self.NextTab()
				else: return
		g.UpdateTabs()



	def shortcuts(self, event):
		if event.GetKeyCode() == wx.WXK_F2:
			SwitchLangs()
		if event.altDown:
			if event.GetKeyCode()==wx.WXK_RIGHT:
				self.NextTab()
			elif event.GetKeyCode()==wx.WXK_LEFT:
				self.PreviousTab()
			elif event.GetKeyCode() == wx.WXK_UP:
				self.FirstTab()
			elif event.GetKeyCode() == wx.WXK_DOWN:
				self.LastTab()
			elif event.GetKeyCode() == ord("R"):
				self.RestoreText()
		elif event.controlDown:
			if event.GetKeyCode() == ord("W"):
				self.CloseTab()
#			elif event.GetKeyCode()==ord("I"):
#				text_viewer.viewer(self, _("text info"), _("text info"), self.textField.GetInfo())
		event.Skip()



app=wx.App()
file = None
if len(sys.argv)>=2:
		if os.path.isfile(sys.argv[1]):
			file = sys.argv[1]
		else:
			if not sys.argv[1]=="None":
				ask = wx.MessageDialog(None, _("Cannot find the {f} file\n do you want to create it now?").format(f=sys.argv[1]), _("file not found"), style=wx.YES_NO+wx.CANCEL)
				ask.SetYesNoCancelLabels(_("yes"), _("no"), _("cancel"))
				result = ask.ShowModal()
				if result ==wx.ID_YES:
					file = sys.argv[1]
					open(file, "w", encoding="utf-8").close()
				elif result == wx.ID_CANCEL:
					sys.exit()
notepad(file)
app.MainLoop()