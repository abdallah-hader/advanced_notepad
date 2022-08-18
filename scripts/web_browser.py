import platform
import webbrowser

def Open(url):
	if platform.system() == 'Windows':
		browser = webbrowser.get('windows-default')
	else:
		browser = webbrowser
	browser.open_new_tab(url)
