#!/usr/bin/env python
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2010 Asymptopia Software

    License         :GPL2

***********************************************************/
"""
import os,sys,string,time
from MultiplicationStation.mstation import *

def usage():
	msg="""
Usage: mstation [OPTION]
	Available options are:
	-help				Show this help
	-wx					Enable the wx admin interface

Example:
	./mstation -wx
	
	"""
	print msg
	

if __name__ == "__main__":
	appdir='MultiplicationStation'
	
	if len(sys.argv)==1:
		x=MultiplicationStationApp()
	elif sys.argv[1]=='-help':
		usage()
	elif sys.argv.count('-wx')>0:
		from MultiplicationStation.mstation_wx import *
		x=MultiplicationStationAppWX()
	else:
		x=MultiplicationStationApp()
