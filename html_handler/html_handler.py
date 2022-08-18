"""
Here, I put everything related to html, creating links, headings, and so on.
I tried to think of how to make a one dialog display to the user for get information, but I failed, so I made a dialog for everything it needed.
Mechanism of Action.
Since I don't like writing comments very much because I can't write them.
I will explain the idea of ​​this file.
First of all, the existing functions each have a function.
For example, the CreateUrl function is specialized in creating links, and it accepts various parameters including link, name, etc., the function will return the result.
Then we will find a class for the dialogue that appears to the user, through which he can fill in the required information, then press create, it will write in the edit field the link obtained from the function, and so on with other things.
"""
import wx
from scripts.Speak import speak
from gui.input_dialog import InputDialog

def CreateHeading(level, text):
	return f"<h{level}>{text}</h{level}>"

def CreateParagraph(text):
	return f"<p>{text}</p>"

def CreateUrl(url, label, inNewTab=False, type=0):
	if type==0:
		if inNewTab:
			result = f"<a href=\"{url}\" target=_blank\">{label}</a>"
		else:
			result = f"<a href=\"{url}\">{label}</a>"
	if type==1:
		result = f"<form method=\"get\" action=\"{url}\"><button type=\"submit\">{label}</button></form>"
	elif type ==2:
		result = f"<a href=\"{url}\"><img src=\"{label}\"/></a>"
	return result

def CreateList(lst, ordered=False):
	result = "<ol>\n" if ordered else "<ul>\n"
	for item in lst:
#		item = item.replace("\\n", "</br>")
		if item==lst[-1]:
			result = result+f"<li>{item}</li>\n</ol>" if ordered else result+f"<li>{item}</li>\n</ul>"
		else:
			result = result+f"<li>{item}</li>\n"
	return result.strip()

class ListsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("create list"))
		p =wx.Panel(self)
		self.CenterOnParent()
		self.SetupContext()
		wx.StaticText(p, -1, _("items list"))
		self.lst = wx.ListBox(p, -1)
		wx.StaticText(p, -1, _("write the new item here"))
		self.textField = wx.TextCtrl(p, -1, style=wx.TE_MULTILINE+wx.HSCROLL)
		add = wx.Button(p, -1, _("add"))
		self.ordered = wx.CheckBox(p, -1, _("ordered list"))
		create = wx.Button(p, -1, _("create"))
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
#		self.textField.Bind(wx.EVT_KEY_DOWN, self.OnShortcuts)
		add.Bind(wx.EVT_BUTTON, self.OnAdd)
		add.SetDefault()
		create.Bind(wx.EVT_BUTTON, self.OnCreate)
		self.ShowModal()

	def OnCreate(self, event):
		if not self.lst.Strings:
			self.textField.SetFocus()
			return speak(_("You must add at least one item."))
		result = CreateList(self.lst.Strings, self.ordered.Value)
		self.Parent.textField.WriteText(result)
		self.Destroy()

	def OnAdd(self, event):
		if not self.textField.Value: return
		self.lst.Append(self.textField.Value.replace("\n", "</br>"))
		self.textField.Clear()
		self.textField.SetFocus() if not self.FindFocus()==self.textField else None

	def SetupContext(self):
		menu = wx.Menu()
		delete = menu.Append(-1, _("delete item"))
		edit = menu.Append(-1, _("edit item"))
		def popup():
			if self.lst.Selection==-1: return
			self.PopupMenu(menu)
		self.Bind(wx.EVT_CONTEXT_MENU, lambda e:popup())
		self.Bind(wx.EVT_MENU, self.OnDelete, delete)
		self.Bind(wx.EVT_MENU, self.OnEdit, edit)

	def OnEdit(self, event):
		current = self.lst.Selection
		new = InputDialog(self, _("edit"), _("edit"), True, self.lst.StringSelection).result
		if not new: return
		self.lst.Delete(current)
		self.lst.Insert(new, current)
		self.lst.Selection = current

	def OnDelete(self, event):
		msg = wx.MessageDialog(self, _("Are you sure you want to remove {item} from the list?").format(item=self.lst.StringSelection), _("delete item"), style=wx.YES_NO)
		msg.SetYesNoLabels(_("yes"), _("no"))
		result = msg.ShowModal()
		self.lst.Delete(self.lst.Selection) if result == wx.ID_YES else None

#	def OnShortcuts(self, event):
#		if event.controlDown and event.GetKeyCode()==wx.WXK_RETURN:
#			self.OnAdd(None)
#		event.Skip()

class ParagraphsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("create paragraph"))
		p = wx.Panel(self)
		self.CenterOnParent()
		wx.StaticText(p, -1, _("paragraph text"))
		self.text = wx.TextCtrl(p, -1, style=wx.TE_MULTILINE+wx.HSCROLL)
		create = wx.Button(p, -1, _("create"))
		create.Bind(wx.EVT_BUTTON, self.OnCreate)
		create.SetDefault()
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		self.ShowModal()

	def OnCreate(self, event):
		if not self.text.Value:
			self.text.SetFocus()
			return speak(_("You must write a text"))
		result = CreateParagraph(self.text.Value.replace("\n", "</br>"))
		self.Parent.textField.WriteText(result)
		self.Destroy()

class UrlsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("create URL"))
		p = wx.Panel(self)
		self.CenterOnParent()
		self.type = wx.RadioBox(p, -1, _("Choose the type of URL"), choices=[_("normal URL"), _("URL button"), _("image URL")])
		self.type.Bind(wx.EVT_RADIOBOX, self.OnChange)
		self.l=wx.StaticText(p, -1, _("name"))
		self.name = wx.TextCtrl(p, -1)
		wx.StaticText(p, -1, _("URL"))
		self.url = wx.TextCtrl(p, -1)
		self.inNewTab = wx.CheckBox(p, -1, _("the URL open in new tab"))
		create = wx.Button(p, -1, _("create"))
		create.Bind(wx.EVT_BUTTON, self.OnCreate)
		create.SetDefault()
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		self.ShowModal()

	def OnChange(self, event):
		if self.type.Selection ==2:
			self.l.SetLabel(_("image URL"))
		else:
			self.l.SetLabel(_("name"))
		if self.type.Selection==0:
			self.inNewTab.Show()
		else: self.inNewTab.Hide()

	def OnCreate(self, event):
		if not self.url.Value:
			self.url.SetFocus()
			return speak(_("You must type the URL."))
		elif not self.name.Value:
			self.name.SetFocus()
			return speak(_("This field is required."))
		result = CreateUrl(self.url.Value, self.name.Value, self.inNewTab.Value, self.type.Selection)
		self.Parent.textField.WriteText(result)
		self.Destroy()

class HeadingsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("create heading"))
		p = wx.Panel(self)
		self.CenterOnParent()
		wx.StaticText(p, -1, _("heading level"))
		self.level = wx.Choice(p, -1, choices=[str(l) for l in range(1,7)])
		wx.StaticText(p, -1, _("the heading text"))
		self.text = wx.TextCtrl(p, -1)
		self.level.Selection = 0
		create = wx.Button(p, -1, _("create"))
		create.Bind(wx.EVT_BUTTON, self.OnCreate)
		create.SetDefault()
		wx.Button(p, wx.ID_CANCEL, _("cancel"))
		self.ShowModal()

	def OnCreate(self, event):
		if self.text.Value == "":
			self.text.SetFocus()
			return speak(_("You must write a text"))
		heading = CreateHeading(self.level.Selection+1, self.text.Value)
		self.Parent.textField.WriteText(heading)
		self.Destroy()

