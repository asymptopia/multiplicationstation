"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2015 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import wx
import os,string
from random import random
import ColorPanel

class CfgCtrl(wx.Panel):
	def __init__(self,admin,nb):
		self.admin=admin
		self.global_config=admin.global_config
		wx.Panel.__init__(self,nb,wx.NewId(),wx.DefaultPosition,wx.DefaultSize,style=wx.FULL_REPAINT_ON_RESIZE)
	
	def setup(self,name):
		self.name=name	
		self.SetBackgroundColour(wx.Colour(0,100,100))
		self.sizer=wx.BoxSizer(wx.VERTICAL);
		
		
		
		"""
		editor=wx.TextCtrl(self,wx.NewId(),style=wx.TE_MULTILINE|wx.TE_PROCESS_TAB)
		inf=open(os.path.join(self.admin.env.sitepkgdir,self.global_config['APPNAME'],'LICENSE'))
		gpl=inf.read()
		inf.close()
		editor.WriteText(gpl)
		editor.SetEditable(0)
		editor.SetSizer(self.sizer)
		self.sizer.Add(editor,0,wx.EXPAND,0)
		"""


		
