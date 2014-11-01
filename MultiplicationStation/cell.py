import sys,os,string,time
from random import random
from string import *

import pygame
from pygame.locals import *

class cell:

	def __init__(self,parent,global_config,rect,tlcx,tlcy,value,correct):
		
		
		self.rect=rect
		self.tlcx=tlcx
		self.tlcy=tlcy
		self.value=value
		
		font=pygame.font.Font(
			os.path.join(parent.env.fontdir,'Font',global_config['FONT_TILE']['value']),
			global_config['FONTSIZE_TILE']['value']
		)
		
		#bgcolor=global_config['bgcolor']
		bg=global_config['COLOR_BG_TILE']['value']
		fg=global_config['COLOR_FG_TILE']['value']
		hi_bg=global_config['COLOR_BG_TILE_HI']['value']
		hi_fg=global_config['COLOR_FG_TILE_HI']['value']
		win_bg=global_config['COLOR_BG_TILE_WIN']['value']
		win_fg=global_config['COLOR_FG_TILE_WIN']['value']
		
		self.surf1=pygame.Surface(rect).convert()
		#self.surf1.fill(bgcolor,(0,0,rect[0],rect[1]))
		self.surf1.fill(bg,(1,1,rect[0]-2,rect[1]-2))
		self.surf1.set_alpha(global_config['COLOR_TILE_ALPHA']['value'])
		
		self.surf2=pygame.Surface(rect).convert()
		#self.surf2.fill(bgcolor,(0,0,rect[0],rect[1]))
		self.surf2.fill(bg,(1,1,rect[0]-2,rect[1]-2))
		self.surf2.set_alpha(global_config['COLOR_TILE_ALPHA']['value'])
		
		font_surface=font.render(`value`,1,fg,bg)
		x_border=int((rect[0]-font_surface.get_rect()[2])/2)
		y_border=int((rect[1]-font_surface.get_rect()[3])/2)
		self.surf2.set_alpha(global_config['COLOR_TILE_ALPHA']['value'])
		self.surf2.blit(font_surface,(x_border,y_border))
		
		self.surf3=pygame.Surface(rect).convert()
		#self.surf3.fill(bgcolor,(0,0,rect[0],rect[1]))
		self.surf3.fill(hi_bg,(1,1,rect[0]-2,rect[1]-2))
		self.surf3.set_alpha(global_config['COLOR_TILE_ALPHA']['value'])
		self.surf3.blit(font.render(`value`,1,hi_fg,hi_bg),(x_border,y_border))
		

		self.surf4=pygame.Surface(rect).convert()
		self.surf4.fill(win_bg,(1,1,rect[0]-2,rect[1]-2))
		self.surf4.set_alpha(global_config['COLOR_TILE_ALPHA']['value'])
		self.surf4.blit(font.render(`value`,1,win_fg,win_bg),(x_border,y_border))

		self.correct=correct
		if self.correct==True:self.surf=self.surf1
		else:self.surf=self.surf2
		self.surf=self.surf1

	def toggle_win(self):
		self.surf=self.surf4

	def toggle_hi(self):
		self.surf=self.surf3
			
	def toggle_lo(self):
		if self.correct:self.surf=self.surf2
		else:self.surf=self.surf1
	
	def set_correct(self):
		self.correct=True
		self.surf=self.surf2

