import pyperclip
import wx
import os
from datetime import datetime
from scripts import backup
from scripts.Speak import speak
from winsound import PlaySound
from settingsconfig import get


translating = False # a variable use to check if translate selection text is already executing.
seconds = 0 #variable to count seconds of translation time to stop it when it reach 15 this work with selection text translation only.
newTab = False # a variable to check if wrighting in new tab or a file
activeFile = None # a variable to keep current loaded file
tabIndex = -1
tabs = dict()
paths = list()
appInfo=None

def ChangeTitle(title=None): # a function to change current title to active file name or any title
	if not title ==None:
		wx.GetApp().GetTopWindow().Title = _("{fn} - {pn}").format(fn=title, pn=appInfo.name) if title else appInfo.name
		return
	global activeFile
	wx.GetApp().GetTopWindow().Title = f"{os.path.basename(activeFile)} - {appInfo.name}"

def UpdateTabs():
	global tabs, paths
	tabs = backup.backup().get()
	try:
		paths = [path for path in tabs]
	except: pass

def GetTime(): # returns the date with time
	time = datetime.now().strftime("%d-%m-%Y - %H_%M_%S")
	return time

def playsound(fn):
	return PlaySound(os.path.join("sounds", fn), 1)

def copy(text):
	return pyperclip.copy(text)

def AddCopy(text):
	if not text:
		return speak(_("You must select text to copy."))
	mark = ""
	if int(get("copymark")) == 1:
		mark = "\\n"
	elif int(get("copymark")) == 2:
		mark = ","
	elif int(get("copymark")) == 3:
		mark = " "
	if not wx.TheClipboard.IsOpened():
		wx.TheClipboard.Open()
	textOBJ = wx.TextDataObject()
	success = wx.TheClipboard.GetData(textOBJ)
	if not success:
		wx.TheClipboard.Close()
		return speak(_("There is no text in the clipboard to do add copy."))
	else:
		textOBJ.SetText(f"{textOBJ.GetText()}{mark}{text}")
		wx.TheClipboard.SetData(textOBJ)
		wx.TheClipboard.Close()
	speak(_("add copied."))

def paste():
	return pyperclip.paste()

def split(txt, factor=10): # function to split text to parts by length giving.
	from scripts.Speak import speak
#	speak("start spliting")
	words = txt.split(" ")
	count = 0
	parts = []
	part = ""
#	("قبل حلقة وايل")
	while count < len(words):
		word = words[count]
		if len(f"{part} {word}") <= factor:
#			speak("بدى ال if الاولا")
			part = f"{part} {word}"
			count += 1
#			speak("نهاية ال if الاولا")
		else:
#			speak("بداية ال else")
			parts.append(part.strip())
			part = ""
			word = words[count]
			count += 1
#			speak("بنهاية ال else")
	if part:
#		speak("بداية ال if الثانية")
		parts.append(part.strip())
#		speak("انتهت ال if 2")
#	speak("قبل الريترن")
	return parts

