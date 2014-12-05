"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2015 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import os,sys,string,time
import wx
#import wx.lib.flatnotebook as fnb
from cfgctrl import *

DEBUG=1

class wxAdmin(wx.Dialog):
	
	def __init__(self,parent):
		
		self.cfgctrl=None
		self.lhp_gif=None
		self.splitter=None
		self.simulator=None
		
		self.parent		=parent
		self.env		=parent.env
		self.configdir	=self.env.configdir
		self.sitepkgdir	=self.env.sitepkgdir
		self.homedir	=self.env.homedir
		self.global_config=self.parent.global_config
		
		wx.Dialog.__init__(
			self,None,wx.NewId(),
			self.global_config['APPNAME'],
			size=wx.Size(self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']),
			style=wx.RESIZE_BORDER|wx.CAPTION|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX
		)
	
	def reload_config(self):
		self.parent.reload_configs
		self.global_config=self.parent.global_config
		
	def setup(self):
		sty = wx.BORDER_SUNKEN
		splitter = wx.SplitterWindow (self,wx.NewId(),style=sty)#|wxSP_3D
		splitter.SetMinimumPaneSize(140)
		lhp=wx.Window(splitter,wx.NewId())
		rhp=wx.Window(splitter,wx.NewId())
		
		fbox=wx.BoxSizer(wx.HORIZONTAL)
		fbox.Add(rhp,1,wx.GROW)
		self.SetSizer(fbox)
		self.SetAutoLayout(True)
		####fbox.Fit(self)
		fbox.Layout()
		
		
		lhp.SetSize((self.global_config['SPLITTER_OFFSET']['value'],600))
		lhp.SetBackgroundColour((255,255,255))
		sidebar_fname=self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['value']
		if DEBUG:print 'sidebar_fname=',sidebar_fname
		sidebar_fname=os.path.join(self.env.sitepkgdir,self.parent.global_config['IMAGE_ADMIN_SIDEBAR']['path'],sidebar_fname)
		if DEBUG:print 'sidebar_fname=',sidebar_fname
		lhp_gif=wx.Image(sidebar_fname,wx.BITMAP_TYPE_GIF).ConvertToBitmap()
		wx.StaticBitmap(lhp,wx.NewId(),lhp_gif,(0,0))
		self.lhp_gif=lhp_gif
		
		size=wx.Size(self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value'])
		self.SetSize(size);
		
		splitter.SplitVertically(lhp,rhp,lhp.GetSize()[0])
		splitter.SetSashPosition(lhp.GetSize()[0]);
		
		
		tabs=['GPL']#'Globals','Readme','Asymptopia',
		nb=wx.Notebook(rhp,wx.NewId(),style=wx.NB_TOP|wx.NB_FIXEDWIDTH)
		print '1'
		
		for idx in range(len(tabs)):
			print '2'
			cfgctrl=CfgCtrl(self,nb)
			print '3'
			nb.AddPage(cfgctrl,tabs[idx],0)
			print '4'
			cfgctrl.setup(tabs[idx])
			print '5'
		
		print '6.0'
		rhpbox=wx.BoxSizer(wx.VERTICAL);
		print '6.1'
		rhpbox.Add(nb,1,wx.EXPAND);
		print '6.2'
		rhp.SetSizer(rhpbox);
		print '6.3'
		rhp.SetAutoLayout(True);
		print '6.4'
		rhpbox.Fit(rhp);
		print '7'
		rhpbox.Layout();
		print '8'
