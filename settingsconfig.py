import configparser
import os

spath=os.path.join(os.getenv("appdata"), "advanced_notepad")
datapath=os.path.join(spath, "backup").replace("\\", "/")

defaults={
	"language":"en",
	"cfu":True,
	"navigateEffects":True,
	"translatefrom":0,
	"translateTo":"english",
	"trfrom":0,
	"trto":"english",
	"getselectedtranslation":0,
	"copymark":0,
	"autosave":1
}

def s_to_b(what):
	if what=="True":
		return True
	elif what=="False":
		return False
	else:
		return what

def init_config():
	init_sections()
	try:
		os.mkdir(spath)
	except FileExistsError:
		pass
	try:
		os.mkdir(datapath)
	except FileExistsError:
		pass
	if not os.path.exists(os.path.join(spath, "settings.ini")):
		config=configparser.ConfigParser()
		config.add_section("settings")
		for k,v in defaults.items():
			config["settings"][k]=str(v)
		with open(os.path.join(spath, "settings.ini"),"w") as f:
			config.write(f)

def init_sections():
	sections=["settings"]
	if not os.path.exists(os.path.join(spath, "settings.ini")): return
	config=configparser.ConfigParser()
	config.read(os.path.join(spath, "settings.ini"))
	for section in sections:
		if config.has_section(section): continue
		config.add_section(section)
	with open(os.path.join(spath, "settings.ini"),"w") as f:
		config.write(f)



def get(string, section="settings"):
	config=configparser.ConfigParser()
	try:
		config.read(os.path.join(spath, "settings.ini"))
		v=config[section][string]
		return s_to_b(v)
	except KeyError:
		if section=="settings":
			new(string, defaults[string])
			return defaults[string]


def new(key, value, section="settings"):
	config = configparser.ConfigParser()
	try:
		config.read(os.path.join(spath, "settings.ini"))
		config[section][key] = str(value)
		with open(os.path.join(spath, "settings.ini"), "w") as f:
			config.write(f)
	except:
		pass