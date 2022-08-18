class info:# program information
	def __init__(self):
		self.name = _("advanced notepad")
		self.version = 1.0
		self.author = _("abdallah hayder")
		self.telegram = "https://t.me/abdallah_alanbry"
		self.facebook = "https://m.facebook.com/profile.php?id=100009657259379"
		self.twitter = "https://twitter.com/abdallahhayder5"
		self.tchannel = "https://t.me/mediaplayerpro"
		self.about= _("""name: {name}.
version: {version}.
author: {author}.
description: A text editor designed for screen reader users.
This editor makes it easy and smooth to control text files with the many features it offers.
Such as the tabs system, save the edited text in the tab, and some ready-made HTML codes. and more.""").format(name=self.name, version=self.version, author=self.author)