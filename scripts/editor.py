"""
this file manage the custom TextCtrl via add some functions to it to load file etc.
"""
import wx
import os
from .import backup
import globals as g
import shelve
from settingsconfig import get, datapath
from .Speak import speak
from datetime import datetime
from .import finder
import application
from gui import text_viewer

class TextBox(wx.TextCtrl): #the custom class for the text box
	def __init__(self, *args, **kwargs):
		super().__init__(style=wx.TE_MULTILINE+wx.HSCROLL+wx.TE_PROCESS_TAB, *args, **kwargs)
		self.__oldContent = self.Value
		self.loaded = False
		self.Bind(wx.EVT_TEXT, self.OnWrite) if int(get("autosave"))==1 else None# bind the edit box to save any thing written to the backup file in the updata
		self.Bind(wx.EVT_KEY_DOWN, self.OnShortcuts)

	@property
	def modified(self):
		return self.__oldContent!=self.Value

	@modified.setter
	def modified(self, value):
		if not value:
			self.__oldContent = self.Value
		else:
			raise ValueError("error with set value")

	def GetInfo(self):
		if self.Value =="": return speak(_("there is no text to get its info."))
		wordsList = self.Value.split()
		characters = len(self.Value)
		words = len(wordsList)
		lines = self.NumberOfLines
		frequentWord = max(wordsList, key=wordsList.count)
		wordRepeted = wordsList.count(frequentWord)
		urlCount = len(finder.FindUrls(self.Value))
		emailsCount = len(finder.FindEmails(self.Value))
		if emailsCount>0:
			emailsCount = _("emails count: {c}.").format(c=emailsCount)
		else:
			emailsCount=""
		if urlCount>0:
			urlCount = _("links count: {c}.").format(c=urlCount)
		else:
			urlCount=""
		info =_("""text info:
Character count: {charCount}.
words count: {wrdCount}.
lines count: {lnsCount}
Most frequent word: {frequent} Which was repeated {repeted} times.
{urlsc}
{emailsc}
 """).format(charCount=characters, wrdCount=words, lnsCount=lines, frequent=frequentWord, repeted=wordRepeted, urlsc=urlCount, emailsc=emailsCount)
		return info.strip()

	def OnShortcuts(self, event):
		key = event.GetKeyCode()
		if key == wx.WXK_F5:
			self.WriteTime()
		elif key == wx.WXK_UP or key == wx.WXK_DOWN:
			self.SavePosition()
		elif event.altDown and event.GetKeyCode()==ord("I"):
			text_viewer.viewer(self, _("text info"), _("text info"), self.GetInfo())
		if int(get("autosave"))==2:
			if event.GetKeyCode()==wx.WXK_SPACE:
				self.OnWrite(None)
		event.Skip()

	def SavePosition(self):
		try:
			try:
				g.tabs[g.activeFile]["line"] = self.PositionToXY(self.InsertionPoint)[-1]
			except KeyError:
				g.tabs[g.paths[g.tabIndex]]["line"] = self.PositionToXY(self.InsertionPoint)[-1]
			backup.backup().UpdateAll(g.tabs)
		except: pass


	def WriteTime(self, event=None):
		date = datetime.now().strftime("%I:%m %p %d/%m/%Y")
		self.WriteText(date)
		speak(_("The time has been written successfully"))


	def OnWrite(self, event):
		if not self.loaded: return # check if the file has been loaded
		try:
			g.tabs[g.activeFile]["value"] = self.Value
			g.tabs[g.activeFile]["line"] = self.PositionToXY(self.InsertionPoint)[-1]
		except KeyError:
			g.tabs[g.paths[g.tabIndex]]["value"] = self.Value
			g.tabs[g.paths[g.tabIndex]]["line"] = self.PositionToXY(self.InsertionPoint)[-1]
		except: pass
		backup.backup().UpdateAll(g.tabs)

	def NewTab(self):
		self.clear()
		number = 1
		numbers = []
		for tab in g.tabs:
			if g.tabs[tab]["newTab"]:
				try:
					numbers.append(int(g.tabs[tab]["path"].split(" (")[1].split(")")[0]))
				except: pass
		numbers.sort()
		for n in numbers:
			if number==n:
				number=n+1
				continue
			else:
				break
		fileName = _("new file ({num})").format(num=number)
		backup.backup().new(fileName, self.Value, True)
		g.UpdateTabs()
		g.tabIndex = g.paths.index(fileName)
		g.ChangeTitle(fileName)
		speak(fileName)
		g.newTab = True
		self.loaded = True

	def clear(self):
		self.loaded = False
		self.Value = ""
		self.__oldContent = ""
		g.activeFile = None
		g.newTab = False
		g.tabIndex = 0
		g.ChangeTitle("")

	def load_file(self, path):
		self.clear()
		path = path.replace("\\", "/")
		self.Value = ""
		self.__oldContent = ""
		g.last = path
		with shelve.open(os.path.join(datapath, "backup")) as f:
			f["last"] = g.last
		if path in g.tabs:
			if not os.path.isfile(path) and not g.tabs[path]["newTab"]:
				msg = wx.MessageBox(_("The file {f} doesn't exist anymore. do you want Keep this file in editor?").format(f=path), _("Keep non existing file"), style=wx.YES_NO, parent=self.Parent)
				if msg == wx.NO:
					backup.backup().delete(path)
					self.Parent.Parent.NextTab()
					return
				else:
					g.tabs[path]["newTab"] = True
					backup.backup().UpdateAll(g.tabs)
					g.UpdateTabs()
			self.Value = g.tabs[path]["value"]
			self.__oldContent = g.tabs[path]["value"]
			try:
				self.InsertionPoint = self.XYToPosition(1, g.tabs[path]["line"])
			except: pass
			if g.tabs[path]["newTab"]:
				g.activeFile = None
				try:
					fn = os.path.basename(g.tabs[path]["path"])
				except:
					fn = g.tabs[path]["path"]
				g.ChangeTitle(fn)
				g.newTab = True
				self.loaded = True
				g.UpdateTabs()
				g.tabIndex = g.paths.index(path)
				return
		else:
			try:
				with open(path, "r", encoding="utf-8") as f:
					self.Value = f.read()
					self.__oldContent = f.read()
			except:
				with open(path, "r", encoding="ansi") as f:
					self.Value = f.read()
					self.__oldContent = f.read()

		backup.backup().new(path, self.Value, line=self.PositionToXY(self.InsertionPoint)[-1])
		g.activeFile = path
		g.ChangeTitle()
		g.newTab = False
		g.UpdateTabs()
		g.tabIndex = g.paths.index(path)
		self.loaded = True

