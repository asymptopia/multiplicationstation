#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2010 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
import wx
from wxadmin import *
from mstation import *

class MultiplicationStationAppWX(wx.App):
	
	def __init__(self):
		wx.App.__init__(self, 0)
		
		mode=0
		fs=-1
		
		while True:
			
			prog=MultiplicationStation(mode,fs,True)
			mode,fs=prog.run()
			
			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:pass#prog.update_highscores()
			elif mode==2:
				rval=prog.admin.ShowModal()
				mode=0
