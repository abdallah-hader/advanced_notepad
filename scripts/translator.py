"""
some functions use to translate text here.
"""
import googletrans
import globals as g
from settingsconfig import get, new
from threading import Thread
from .Speak import speak
translator = googletrans.Translator()

def translate(text, From=None, to="en", selection=False): # this function translate the text also it will check if the length of the content more than 5000 characters it will make it parts then translate and return it.
	if not text:
		g.translating = False
		return speak(_("There is no text to translate."))
	global translator
	translated = ""
	if not From or From==int(0) or From=='auto detect':
		try:
			From = translator.detect(text).lang
		except: pass
	if not selection:
		new("translatefrom", From)
		new("translateto", to)
	if len(text)>3000:
		tlist = []
		parts = g.split(text, 3000)
		for part in parts:
			try:
				tr = translator.translate(part, src=From, dest=to).text
				tlist.append(tr)
			except: continue
		translated = "\n".join(tlist)
	else:
		try:
			translated = translator.translate(text, src=From, dest=to).text
		except:
			translated = None
#	if not translated and not selection:
#		return
	if selection:
		if int(get("getselectedtranslation")) == 0:
			speak(translated)
		elif int(get("getselectedtranslation")) == 1:
			speak(translated)
			g.copy(translated)
		else:
			g.copy(translated)
			speak(_("The translation result is copied to the clipboard."))
		g.translating = False
		return
	return translated

def TranslateSelection(text):
	g.translating = True
	From = get("trfrom")
	to = get("trto")
	def beeping():
		from time import sleep
		while g.translating:
			g.playsound("beep.wav")
			g.seconds+=1
			if g.seconds>=15:
				g.seconds = 0
				g.translating = False
				speak(_("An error occurred during the translation process, please try again later."))
				break
			sleep(1)
	Thread(target=beeping).start()
	Thread(target=translate, args=[text, From, to, True]).start()

def SwitchLangs():
	From = get("trfrom")
	to = get("trto")
	new("trfrom", to)
	new("trto", From)
	speak(_("translate: from {f} to {t}").format(f=to, t=From))

def GetLanguages(): #this function returns dictionary and list contains llanguages.
	languages = {v:k for k,v in googletrans.LANGUAGES.items()}
	return languages


