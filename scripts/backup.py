"""
here some functions makes some things easyly and faster to  do. backup of tab or create and restore backups
"""
import wx
import os
import shelve
from settingsconfig import get,new,datapath,spath
import globals as g
import sys
from datetime import datetime
from zipfile import ZipFile

class backup: # the manager for update, create, and delete tabs
	def new(self, path, value, newTab=False, line=0): # a function to create new tab
		with shelve.open(os.path.join(datapath, "backup")) as data:
			try:
				backups = data["backups"]
			except KeyError:
				backups = {}
			backups[path] = {"path":path, "value":value, "newTab":newTab, "line":line}
			data["backups"] = backups
			g.UpdateTabs()

	def get(self): # a function returns the tabs dict if exists or returns empty dict if not exists.
		try:
			with shelve.open(os.path.join(datapath, "backup")) as data:
				tabs = data["backups"]
				return tabs
		except:
				return {}

	def UpdateAll(self, data): # a function to update the tabs dict in the data file.
		with shelve.open(os.path.join(datapath, "backup")) as d:
			d["backups"] = data

	def delete(self, tab): # deletes a tab from data file
		with shelve.open(os.path.join(datapath, "backup")) as d:
			try:
				data = d["backups"]
				del data[tab]
				d["backups"] = data
				g.UpdateTabs()
			except:
				pass

	def CreateDataBackup(self, Parent):
		dir = wx.DirDialog(Parent, _("select folder to save the new backup file"))
		result = dir.ShowModal()
		if result!=wx.ID_CANCEL:
			os.chdir(spath)
			files = os.listdir()
			if not files: return
			time = datetime.now().strftime(" - %d_%m_%Y %I %p")
			fn = f"backup {time}.zip"
			file = ZipFile(os.path.join(dir.GetPath(),fn), "w")
			for f in files:
				if os.path.isfile(f):
					file.write(f)
				else:
					files2 = os.listdir(f)
					if not files2: continue
					for f2 in files2:
						file.write(os.path.join(f, f2))
			file.close()
		wx.MessageBox(_("Backup created successfully, the backup  path: {p}").format(p=os.path.join(dir.GetPath(), fn)), _("success"), parent=Parent)

	def RestoreBackup(self, Parent):
		path = wx.FileSelector(_("choos a backup to restore"), wildcard="|*.zip", parent=Parent)
		if not path:return
		file = ZipFile(path, "r")
		valid = "backup/backup.bak" in file.namelist() and "settings.ini" in file.namelist()
		if valid:
			msg = wx.MessageBox(_("If you click Yes: the selected backup will be restored, and you cannot undo this action. Are you sure you want to restore the backup?"), _("warning"), style=wx.YES_NO, parent=Parent)
			if msg==wx.YES:
				file.extractall(spath)
				file.close()
				wx.MessageBox(_("The backup has been successfully restored, click OK to restart the program."), _("success"), parent=Parent)
				return os.execl(sys.executable, sys.executable)
		else:
			wx.MessageBox(_("You have selected an invalid backup"), _("error"), style=wx.ICON_ERROR, parent=Parent)