from scripts.Speak import speak
from settingsconfig import get

def GetDoc():
	lang = get("language")
	content = ""
	try:
		with open(f"docs/{lang}/help.txt", "r", encoding="utf-8") as f:
			content = f.read()
		return content
	except:
		speak(_("An error occurred while trying to get the help file."))
		return None