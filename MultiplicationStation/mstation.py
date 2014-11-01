#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
/**********************************************************

    Organization    :AsymptopiaSoftware | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@gmail.com

    Copyright       :(C) 2006-2010 Asymptopia Software

    License         :GPLv3

***********************************************************/
"""
from random import *

import pygame
from pygame.locals import *
import unicodedata

from button import *
from player import *
from cell import *
from environment import *
from dict_formatter import *
from projectile import *

DEBUG=0

global images
images={}

class MultiplicationStationApp:
	
	def __init__(self):
		
		mode=0
		fs=-1
		
		while True:
			
			prog=MultiplicationStation(mode,fs,False)
			mode,fs=prog.run()
			
			if mode<0:prog.on_exit()
			elif mode==0:pass#prog.update_highscores()
			elif mode==1:pass#prog.update_highscores()
			elif mode==2:
				#rval=prog.admin.ShowModal()
				mode=0
			
			
			
class MultiplicationStation:
	
	global images
	
	def __init__(self,mode,fs,USE_WX):
	
		if USE_WX:
			import wxadmin
			from wxadmin import wxAdmin

		self.MODE=mode
		
		self.player_idx=0
		
		self.W=None
		self.H=None
		self.bkg=None
		self.bgImage=None
		self.screen=None
		
		self.AMFULLSCREEN=fs
		self.MOVIE=0
		
		self.bfont=None
		self.cfont=None
		self.hudfont=None
		self.appnamefont=None
		self.myfont_large=None
		self.myfont_medium=None
		self.myfont_small=None
		self.myfont_xsmall=None
		
		self.submission=None
		self.highscore_surface=None
		
		self.admin_button=None
		self.play_button=None
		self.quit_button=None
		self.skip_button=None
		self.okay_button=None
		
		self.adminbuttongroup=None
		self.adminbuttons=None
		
		self.playbuttongroup=None
		self.playbuttons=None
		
		self.quitbuttongroup=None
		self.quitbuttons=None
		
		self.skipbuttongroup=None
		self.skipbuttons=None
		
		self.okaybuttongroup=None
		self.okaybuttons=None
		
		self.submission=None
		
		self.correct_sound=None
		self.incorrect_sound=None
		
		self.pickup_sounds	=None
		self.release_sounds	=None
		self.lockin_sounds	=None
		self.bounce_sounds	=None
		self.lose_sounds	=None
		self.win_sounds		=None

		self.admin=None
		self.target=None
		self.players=[]
		self.tray_spots=[]
		self.t_last=time.time()
		self.animation_in_progress=0

		self.env=Environment('MultiplicationStation')
		self.env.USE_WX=False
		if USE_WX:self.env.USE_WX=USE_WX

		self.STOP_RUNNING=0
		self.CANNOT_MOVE_COUNT=0
		
		if self.env.OS=='win':
			os.environ['SDL_VIDEODRIVER'] = 'windib'
		pygame.display.init()
		pygame.init()
		pygame.event.set_blocked(MOUSEMOTION)#Wow! this helps!

		self.global_config=self.load_config()
		pygame.display.set_caption(self.global_config['APPNAME'])
		self.target=pygame.sprite.RenderClear()#drag-n-drop object
		
		if self.env.USE_WX:
			self.admin=wxAdmin(self)
			self.admin.setup()
		
		self.SCREENSAVER=self.global_config['SCREENSAVER_ON_AT_START']['value']

		self.operator=None
		self.row=None
		self.col=None
		self.countdown=None
		self.t_session=None

		self.dt_last=None
		self.last_points=None
		self.players=None
		self.move_number=None
		self.answer=None
		self.current_question=None
		self.user_answer=None
		self.correct=None
		self.incorrect=None

		self.light=None
		self.fwoverlay=None
		self.hud_font=None
		self.t_light_on=time.time()

	def handle_mouse(self):	
		
		for event in pygame.event.get(QUIT):
			pygame.quit()
			sys.exit()

		for event in pygame.event.get(MOUSEBUTTONDOWN):
			
			#LOGIN/LOGOUT BUTTON:
			if self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.STOP_RUNNING=1
				self.MODE=1
				return
				
			#CHECK FOR BUTTON PRESS
			elif self.admin_button.rect.collidepoint(pygame.mouse.get_pos()):
				self.AMFULLSCREEN=0
				self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
				#self.animation_in_progress=0
				self.MODE=2
				self.STOP_RUNNING=1
				return
				
			elif self.play_button.rect.collidepoint(pygame.mouse.get_pos()) and self.MODE==0:
				self.MODE=1
				self.STOP_RUNNING=1
				if DEBUG:print 'play button pressed'
				
			if self.MODE==0:return
			

	def handle_keyboard(self):			
		
		for event in pygame.event.get(QUIT):
			pygame.quit()
			sys.exit()

		if not self.current_question:return
		
		digits=['0','1','2','3','4','5','6','7','8','9']
		allowed=['0','1','2','3','4','5','6','7','8','9','+','-']
		
		if self.MODE==0:
			uidx=len(self.current_question['user_answer'])
			aidx=len(self.current_question['answer'])
			if uidx<aidx:
				if self.current_question['answer'][uidx]=='-':
					kval="K_KP_MINUS"
				else:
					kval="K_%s"%(self.current_question['answer'][uidx])
				
				event=pygame.event.Event(KEYDOWN,{'key':eval(kval)})
			else:
				event=pygame.event.Event(KEYDOWN,{'key':13})
			
			pygame.event.post(event)
			if DEBUG:print 'event:',event
		
		for event in pygame.event.get(KEYDOWN):
			
			if pygame.key.name(event.key)==K_BACKSPACE or pygame.key.name(event.key)=='backspace':
				self.current_question['user_answer']="%s"%(self.current_question['user_answer'][:-1])
			
			elif event.key==K_F11:
				try:self.take_screenshot()
				except:pass
			
			elif event.key==K_F9:
				self.go_help()
				
			elif event.key==K_F10:
				self.go_credit()
			
			elif event.key==K_F12:
				try:
					self.AMFULLSCREEN*=-1
					pygame.display.toggle_fullscreen()
				except Exception,e:
					pass
					
			elif event.key == K_ESCAPE:
				self.MODE-=1
				self.STOP_RUNNING=1
				return
			
			elif event.type == QUIT:self.STOP_RUNNING=-1#unused?
				
			elif event.key==13 or pygame.key.name(event.key)=='enter':
				self.READY=1
			else:
		
				try:
					
					submission=pygame.key.name(event.key)
					submission=string.replace(submission,'[','')
					submission=string.replace(submission,']','')
					dummy=allowed.index(submission)
					if event.key==K_KP_MINUS or event.key==K_MINUS:
						if self.current_question['user_answer'].count('-'):continue#disallow multiple minuses
						if len(self.current_question['user_answer'])>0:continue#minus only allowed as first character
					self.current_question['user_answer']="%s%s"%(self.current_question['user_answer'],submission)
					
				except Exception,e:
					
					if DEBUG:print e
					pass
					

	def reset_grid(self):
		
		self.grid=[]
		
		dx=self.global_config['BOARD_TILESIZE_X']['value']
		dy=self.global_config['BOARD_TILESIZE_Y']['value']
		
		if self.MODE==0:
			
			
			self.global_config['GAME_COL_LOW']['value']=int(random()*12)
			self.global_config['GAME_COL_HIGH']['value']=self.global_config['GAME_COL_LOW']['value']+int(random()*12)
			self.global_config['GAME_ROW_LOW']['value']=-10+int(random()*32)
			self.global_config['GAME_ROW_HIGH']['value']=self.global_config['GAME_ROW_LOW']['value']+int(random()*12)
			self.global_config['GAME_OPERATOR']['value']=int(random()*3)
		
		ncol=(self.global_config['GAME_COL_HIGH']['value']-self.global_config['GAME_COL_LOW']['value'])+2
		nrow=(self.global_config['GAME_ROW_HIGH']['value']-self.global_config['GAME_ROW_LOW']['value'])+2
		
		
		
		self.ncol=ncol
		self.nrow=nrow
		
		
		lhs_offset=(self.global_config['WIN_W']['value']-ncol*dx)/2
		top_offset=(self.global_config['WIN_H']['value']-nrow*dy)/2
		
		
		
		for row in range(0,nrow):
			r=[]
			for col in range(0,ncol):
				
				correct=False
				tlcx=lhs_offset+col*dx
				tlcy=top_offset+row*dy
				
				if row==0 and col==0:
					correct=False
					value=0
				elif row==0:
					correct=True
					value=self.global_config['GAME_COL_LOW']['value']+col-1
				elif col==0:
					correct=True
					value=self.global_config['GAME_ROW_LOW']['value']+row-1
				else:
					correct=False
					#print self.global_config
					a=self.global_config['GAME_ROW_LOW']['value']+row-1
					b=self.global_config['GAME_COL_LOW']['value']+col-1
					
					if self.global_config['GAME_OPERATOR']['value']==0:operator='+'
					elif self.global_config['GAME_OPERATOR']['value']==1:operator='-'
					else:operator='*'

					value=eval(`a`+operator+`b`)
				
				#r.append(cell(self.main,(dx,dy),tlcx,tlcy,value,self.main.tile_font,0))
				r.append(cell(self,self.global_config,(dx,dy),tlcx,tlcy,value,0))
			
			self.grid.append(r)
	
		for col in range(1,ncol):
			try:self.grid[0][col].set_correct()
			except:pass
		
		for row in range(1,nrow):
			try:self.grid[row][0].set_correct()
			except:pass
		

	def make_problems(self):
		problems=[]
		counter=0
		for a in range(self.global_config['GAME_ROW_LOW']['value'],self.global_config['GAME_ROW_HIGH']['value']+1):
			for b in range(self.global_config['GAME_COL_LOW']['value'],self.global_config['GAME_COL_HIGH']['value']+1):
				if a==0 and self.global_config['GAME_SKIP_ZERO']['value']:continue
				if b==0 and self.global_config['GAME_SKIP_ZERO']['value']:continue
				
				if self.global_config['GAME_OPERATOR']['value']==0:
					operator='+'
					unicode_operator=unicodedata.lookup('PLUS SIGN')
				elif self.global_config['GAME_OPERATOR']['value']==1:
					operator='-'
					unicode_operator=unicodedata.lookup('HYPHEN-MINUS')
				else:
					operator='*'
					unicode_operator=unicodedata.lookup('MULTIPLICATION SIGN')
				
				Q="%d %s %d"%(a,unicode_operator,b)
				A="%d"%(eval(`a`+operator+`b`))
				
				problem={'question':Q,}
				problem['user_answer']=''
				problem['answer']=A
				problem['correct']=0
				problem['incorrect']=1
				problem['row']=`a`
				problem['col']=`b`
				
				problems.append(problem)
				
				counter+=1
				
		if self.global_config['GAME_RANDOMIZE']['value']==0:return problems
		for idx in range(len(problems)):
			dummy=int(3*random())
			for idx in range(dummy):dx=random()
			problems.insert(int(random()*len(problems)-1),problems.pop(int(random()*len(problems))))
		return problems
	
	def render_grid(self):
		for row in range(0,self.nrow):
			for col in range(0,self.ncol):
				c=self.grid[row][col]
				self.screen.blit(c.surf,(c.tlcx,c.tlcy))
		
			
	
	def congratulate(self):
		msg=self.appnamefont.render(
			"Congratulations!",1,
			self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG_TILE']['value']
		)
		msg.set_colorkey(self.global_config['COLOR_BG_TILE']['value'])
		
		fw=msg.get_rect()[2]
		fh=msg.get_rect()[3]
		xp=(self.global_config['WIN_W']['value']-fw)/2
		yp=(self.global_config['WIN_H']['value']-fh)/2

		WAITING=True
		t_wait=5
		t0=time.time()
		self.update()
		self.screen.blit(msg,(xp,yp))
		self.flip()
		while WAITING:
			for e in pygame.event.get(KEYDOWN):WAITING=False
			if time.time()-t0>t_wait and self.MODE==0:WAITING=False
		return 0		

	def timer_update(self):
		t_current=time.time()
		self.dt_last=t_current-self.t_last
		self.t_last=t_current
		return self.dt_last
		
	
	def run(self):
		
		if DEBUG:print 'run calling update'
		
		self.update_global_config_dependents()
		if self.MODE==0:self.go_splash()
		
		if self.STOP_RUNNING:return(self.MODE,self.AMFULLSCREEN)
		
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill(self.global_config['COLOR_BG']['value'])#green

		dx=self.global_config['BOARD_TILESIZE_X']['value']
		lhs_offset=(self.global_config['WIN_W']['value']-13*dx)/2
		dy=self.global_config['BOARD_TILESIZE_Y']['value']
		top_offset=(self.global_config['WIN_H']['value']-lhs_offset)/2
		red_light=pygame.Surface((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		red_light.fill(self.global_config['COLOR_CORRECT']['value'])
		
		green_light=pygame.Surface((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		green_light.fill(self.global_config['COLOR_INCORRECT']['value'])
		light=None
		
		if pygame.mixer and self.global_config['SOUNDON']['value']:
			try:
				self.incorrect_sound=pygame.mixer.Sound(self.global_config['GAME_INCORRECT_SOUND'])
				self.correct_sound=pygame.mixer.Sound(self.global_config['GAME_CORRECT_SOUND'])
			except:pass

		#recorder=EduAppRecorder(self,self.global_config,self.global_config)
		#self.recorder=recorder
		self.t0=time.time()
		self.t_session=0
		self.t_last=self.t0
		self.dt_last=0
		#self.move_number=0

		self.reset_grid()
		problems=self.make_problems()
		complete=[]
		
		lone_player=Player('UNUSED',None,None,None)
		#lone_player.recording=self.global_config['RECORDER_ON']['value']
		self.players=[lone_player,]
		
		self.STOP_RUNNING=0
		
		while len(problems)>0:
			
			if self.STOP_RUNNING!=0:
				#self.onexit()
				return(self.MODE,self.AMFULLSCREEN)
			
			while self.light:
				self.update()
				if self.STOP_RUNNING!=0:
					return(self.MODE,self.AMFULLSCREEN)
				
			self.current_question=problems.pop(0)
			self.question_surface=self.question_font.render(self.current_question['question'],1,self.global_config['COLOR_FG_QUESTION']['value'],self.global_config['COLOR_FG_QUESTION']['value'])
			self.question_surface.set_colorkey(self.global_config['COLOR_FG_QUESTION']['value'])
			
			if self.global_config['GAME_OPERATOR']['value']==0:operator='+'
			elif self.global_config['GAME_OPERATOR']['value']==1:operator='-'
			else:operator='*'
			
		   	if DEBUG:print self.current_question
			
			row=eval(self.current_question['row'])-self.global_config['GAME_ROW_LOW']['value']
			col=eval(self.current_question['col'])-self.global_config['GAME_COL_LOW']['value']
			
			self.grid[0][col+1].toggle_hi()
			self.grid[row+1][0].toggle_hi()
			#self.grid[row+1][col+1].toggle_hi()
			
			self.READY=False
			
			while not self.READY:
				self.update()
				if time.time()-self.t_last > self.global_config['GAME_COUNTDOWN']['value']:self.READY=True
				
				if self.STOP_RUNNING!=0:
					#self.onexit()
					return(self.MODE,self.AMFULLSCREEN)
			
			digits=['0','1','2','3','4','5','6','7','8','9']
			digit_count=0
			for idx in range(len(digits)):
				digit_count+=self.current_question['user_answer'].count(digits[idx])
			
			if digit_count==0:
				self.light="red"
				self.current_question['user_answer']=''
				self.t_light_on=time.time()
				self.current_question['correct']=0
				self.current_question['incorrect']=1
				problems.insert(int(random()*len(problems))-1,self.current_question)
			
			elif len(self.current_question['user_answer']) and eval(self.current_question['answer'])==eval(self.current_question['user_answer']):	
				self.grid[row+1][col+1].set_correct()
				self.grid[row+1][col+1].toggle_win()
				self.light="green"
				self.t_light_on=time.time()
				self.current_question['correct']=1
				self.current_question['incorrect']=0
				complete.append(self.current_question)
				
			else:
				self.light="red"
				self.current_question['user_answer']=''
				self.t_light_on=time.time()
				self.current_question['correct']=0
				self.current_question['incorrect']=1
				problems.insert(int(random()*len(problems))-1,self.current_question)
				
			while self.light:
				self.update()#for light
				if self.STOP_RUNNING!=0:
					return(self.MODE,self.AMFULLSCREEN)
	
			
			self.grid[0][col+1].toggle_lo()
			self.grid[row+1][0].toggle_lo()
			self.grid[row+1][col+1].toggle_lo()
			
			t=time.time()
			self.dt_last=t-self.t_last
			self.t_session+=self.dt_last
			self.t_last=t

		self.current_question=None
		rval=self.congratulate()
		self.MODE=0
		
		return(self.MODE,self.AMFULLSCREEN)
	
		
		
	def update(self):

		if self.STOP_RUNNING==1:
			print '1'
			return(self.MODE,self.AMFULLSCREEN)
		self.handle_mouse()
		if self.STOP_RUNNING==1:
			print '2'
			return(self.MODE,self.AMFULLSCREEN)

		self.handle_keyboard()
		pygame.event.clear()
		
		
		self.screen.fill(self.global_config['COLOR_BG']['value'])

		if self.bgImage:self.screen.blit(self.bgImage,(0,0))
		else:self.screen.blit(self.bkg,(0,0))
		
		if self.MODE==1:
			
			if self.light=="green":
				self.screen.fill(self.global_config['COLOR_CORRECT']['value'])
				if pygame.mixer and self.incorrect_sound and self.global_config['SOUNDON']['value']:
					try:self.correct_sound.play()
					except:pass
			elif self.light=="red":
				self.screen.fill(self.global_config['COLOR_INCORRECT']['value'])
				if pygame.mixer and self.correct_sound and self.global_config['SOUNDON']['value']:
					try:self.incorrect_sound.play()
					except:pass
		
		
		self.render_grid()
		#self.screen.blit(self.question_surface,(xlhs,ytop))
		
		if self.MODE==0:self.adminbuttons.draw(self.screen)
		
		if self.current_question:
			rendered_size=self.question_font.size(self.current_question['question'])
			xlhs=self.global_config['WIN_W']['value']/2-rendered_size[0]/2
			ytop=self.global_config['WIN_H']['value']/2-rendered_size[1]
			self.screen.blit(self.question_surface,(xlhs,ytop))
	
			s3=self.submission_font.render(self.current_question['user_answer'],1,self.global_config['COLOR_FG_QUESTION']['value'],self.global_config['COLOR_BG_TILE']['value'])
			s3.set_colorkey(self.global_config['COLOR_BG_TILE']['value'])
			xlhs2=self.global_config['WIN_W']['value']/2-self.submission_font.size(self.current_question['user_answer'])[0]/2
			ytop2=self.global_config['WIN_H']['value']/2
			self.screen.blit(s3,(xlhs2,ytop2))
		
		
		
		
		#HIGH_SCORE_LIST:
		#if self.MODE==0 and self.global_config['GAME_HIGH_SCORE_LIST']:self.blit_high_scores()
		
		if (time.time()-self.t_light_on)>self.global_config['GAME_T_LIGHT']['value']:self.light=None
		
		self.flip()
		
		#if self.global_config['GAME_RECORD_MOVIE']['value']:
		#	oufname="%05d.bmp"%(self.movie_idx)
		#	pygame.image.save(pygame.display.get_surface(),oufname)
		#	self.movie_idx+=1




	def update_global_config_dependents(self):
		
		t0=time.time()
		if DEBUG:print 'update_global_config_dependents 01:',"%3.3f"%(time.time()-t0)
		
		
		#ie adminbutton which is pygame.sprite.RenderPlain(Group..)
		self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
		self.bkg=pygame.Surface(self.screen.get_size())
		self.bkg=self.bkg.convert()
		self.bkg.fill(self.global_config['COLOR_BG']['value'])
		
		if DEBUG:print 'update_global_config_dependents 02:',"%3.3f"%(time.time()-t0)
		
		
		#SET DISPLAY MODE:
		if pygame.display.get_init():
			
			self.screen=pygame.display.set_mode((self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			if self.AMFULLSCREEN==1:pygame.display.toggle_fullscreen()
			
			self.bkg=pygame.Surface(self.screen.get_size())
			self.bkg=self.bkg.convert()
			self.bkg.fill(self.global_config['COLOR_BG']['value'])
			pygame.font.init()
		
		if DEBUG:print 'update_global_config_dependents 03:',"%3.3f"%(time.time()-t0)

		#LOAD FONTS SO CAN DISPLAY PROGRESS MESSAGE:
		if self.env.OS!='win':
			asdf=os.path.join(self.env.fontdir,self.global_config['FONT_BFONT']['path'],self.global_config['FONT_BFONT']['value'])
			self.bfont=pygame.font.Font(
				asdf,
				int(self.global_config['FONTSIZE_BUTTON']['value'])
			)
			
			#self.cfont=pygame.font.SysFont('latin,coptic,cyrillic',self.global_config['FONTSIZE_TILE']['value'],0,0)
			self.cfont=pygame.font.Font(
				os.path.join(self.env.fontdir,self.global_config['FONT_CFONT']['path'],self.global_config['FONT_CFONT']['value']),
				int(self.global_config['FONTSIZE_BUTTON']['value'])
			)
		else:
			self.bfont=pygame.font.Font(
				os.path.join(self.env.fontdir,'Font',self.global_config['FONT_BFONT']['value']),
				int(self.global_config['FONTSIZE_BUTTON']['value'])
			)
			self.cfont=pygame.font.Font(
				os.path.join(self.env.fontdir,'Font',self.global_config['FONT_CFONT']['value']),
				int(self.global_config['FONTSIZE_TILE']['value'])
			)
			
		###
		self.hudfont=pygame.font.Font(
			os.path.join(self.env.fontdir,'Font',self.global_config['FONT_HUD']['value']),
			int(self.global_config['FONTSIZE_HUD']['value'])
		)
		self.appnamefont=pygame.font.Font(
			os.path.join(self.env.fontdir,'Font',self.global_config['FONT_APPNAME']['value']),
			int(self.global_config['FONTSIZE_APPNAME']['value'])
		)
		
		self.question_font=pygame.font.Font(
			os.path.join(self.env.fontdir,'Font',self.global_config['FONT_QUESTION']['value']),
			int(self.global_config['FONTSIZE_QUESTION']['value'])
		)
		self.submission_font=pygame.font.Font(
			os.path.join(self.env.fontdir,'Font',self.global_config['FONT_QUESTION']['value']),
			int(self.global_config['FONTSIZE_QUESTION']['value'])
		)
		
		###
		if DEBUG:print 'update_global_config_dependents 04:',"%3.3f"%(time.time()-t0)

		#ATTEMPT TO LOAD BGIMAGE:
		if self.global_config['IMAGE_BG']['value']!='':
			try:
				self.bgImage=pygame.image.load(os.path.join(self.global_config['IMAGE_BG']['path'],self.global_config['IMAGE_BG']['value']))#os.path.join(self.sitepkgdir,self.global_config['APPNAME'],'Images','sunset01.jpg')
				self.bgImage=pygame.transform.scale(self.bgImage, (self.global_config['WIN_W']['value'],self.global_config['WIN_H']['value']))
			except Exception,e:
				print e
				self.bgImage=None
		if DEBUG:print 'update_global_config_dependents 05:',"%3.3f"%(time.time()-t0)
		
		
		if DEBUG:print 'update_global_config_dependents 09:',"%3.3f"%(time.time()-t0)
		###
		#BUTTONS
		#reveal w.r.t. WIN_W
		reveal=20
		H0=self.global_config['WIN_H']['value']-50#self.board.YBOT
		
		#ADMINBUTTONS
		self.admin_button=Button(self.global_config,'Admin',self.bfont)
		self.admin_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.admin_button.get_width()/2-reveal,
			self.global_config['WIN_H']['value']-self.admin_button.get_height()/2-H0
		)
		
		self.play_button=Button(self.global_config,'Play',self.bfont)
		self.play_button.rect.center=(#NOTE: THIS IS *CENTER*
			self.global_config['WIN_W']['value']-self.admin_button.get_width()/2-reveal,
			self.global_config['WIN_H']['value']-self.admin_button.get_height()/2-H0+50
		)
		
		self.adminbuttongroup=pygame.sprite.Group([self.admin_button,self.play_button])
		self.adminbuttons=pygame.sprite.RenderPlain(self.adminbuttongroup)
		
		

		############END:MSTATION
		#Try to load sounds:
		try:
			self.incorrect_sound=pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','heckel.wav'))
			self.correct_sound	=pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win01.wav'))
			"""
			self.pickup_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','pickup01.wav')),]
			self.release_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','release01.wav')),]
			self.lockin_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','lockin01.wav')),]
			self.bounce_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','bounce01.wav')),]
			self.lose_sounds	=[pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','lose01.wav')),]
			self.win_sounds		=[
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win01.wav')),
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win02.wav')),
									pygame.mixer.Sound(os.path.join(self.env.sitepkgdir,self.global_config['APPDIR'],'Sounds','win03.wav')),
						 		 ]
			"""					 
		except Exception,e:
			self.global_config['SOUNDON']['value']=0
		
		"""
		if self.global_config['DISPLAY_HIGH_SCORES']['value']==1:
			if len(self.global_config['HIGH_SCORES'])>0:
				highscore_string="High Score: %s %d"%(self.global_config['HIGH_SCORES'][0][0],self.global_config['HIGH_SCORES'][0][1])
				self.highscore_surface=self.hudfont.render(highscore_string,1,self.global_config['COLOR_HIGH_SCORES']['value'],self.global_config['COLOR_BG']['value'])
				self.highscore_surface.set_colorkey(self.global_config['COLOR_BG']['value'])
		"""
		
		
		if DEBUG:print 'update_global_config_dependents 10:',"%3.3f"%(time.time()-t0)
		
		
	def flip(self):
		pygame.display.flip()

	def load_config(self):
		
		if DEBUG:print 'mstation.load_config'
		
		configdir	=self.env.configdir
		if DEBUG:print configdir,intermediate_path,fname
		
		homedir=os.getenv('HOME')
		if not homedir:homedir=os.getenv('USERPROFILE')
		infname=os.path.join(homedir,'.mstation_config')
		
		if not os.path.exists(infname):
			master_fname=os.path.join(self.env.fontdir,'.mstation_config_master')
			if self.env.OS=='win':
				cmd="copy %s %s"%(master_fname,os.path.join(homedir,'.mstation_config'))
				if DEBUG:print cmd
				os.system(cmd)
			else:
				cmd="cp %s %s"%(master_fname,os.path.join(homedir,'.mstation_config'))
				if DEBUG:print cmd
				os.system(cmd)
			
		inf=open(infname)
		content=inf.read()
		
		content=string.strip(content)
		
		config=eval(content)
		inf.close()
		return config


	def reload_configs(self):
		if DEBUG:print 'reload_configs:'
		self.global_config=self.load_config()
		
		

	def go_help(self):
		self.screen.fill((0,0,0))
		self.show_help()		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
		
		
		
	def show_help(self):
		
		linesize=self.hudfont.size('-------------------------------------------------------')
		
		msgs=[
			u'-------------------------------------------------------',
			u'                         HELP                          ',
			u'-------------------------------------------------------',
			u'                                                       ',
			u'F9  Key: Show help                                     ',
			u'F10 Key: Show credits                                  ',
			u'F11 Key: Screenshot to HOME directory                  ',
			u'F12 Key: Fullscreen (Linux only)                       ',
			u'ESC Key: Exit                                          ',
			u'                                                       ',
			u'mstation -wx for admin control panel                   ',
		]
		
		y0=self.global_config['WIN_H']['value']/2-len(msgs)/2.*linesize[1]
		fg_hud=None
		bg_hud=None
		
		for msg_idx in range(len(msgs)):
			
			if msg_idx==1:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_HILIGHT']['value']
			else:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_FG_HUD']['value']
			
			bg_hud=self.global_config['COLOR_BG_HUD']['value']
			help_surface=font.render(
				msgs[msg_idx],1,
				fg_hud,
				bg_hud 
			)	
			hs_w=linesize[0]
			hs_h=help_surface.get_size()[1]
			self.screen.blit(help_surface,(self.global_config['WIN_W']['value']/2.-hs_w/2.,y0+msg_idx*linesize[1]))
			

	def go_credit(self):		
		self.screen.fill((0,0,0))
		self.show_credit()		
		self.flip()
		while 1:
			breakout=0
			for event in pygame.event.get([KEYUP]):
				if event.type == KEYUP:breakout=1
				self.KDOWN=0
				self.TDOWN=0
			if breakout:break
		
		
	def show_credit(self):
		
		linesize=self.hudfont.size('text to determine font size')
		
		msgs=[
			u'This software was written for',
			u'Millie and Jordan',
			u'* And * Kids * Everywhere *',
			u'',
			u'MultiplicationStation Version 0.6.2',
			u'January 17, 2010',
			u'',
			u'Author:Charles B. Coss'+u'\xe9',
			u'Contact:ccosse@gmail.com', 
			u'Website: www.asymptopia.org',
		]
		
		y0=self.global_config['WIN_H']['value']/2-len(msgs)/2.*linesize[1]
		fg_hud=None
		bg_hud=None
		
		for msg_idx in range(len(msgs)):
			
			if msg_idx==1:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_HILIGHT']['value']
			else:
				font=self.hudfont
				fg_hud=self.global_config['COLOR_FG_HUD']['value']
			
			bg_hud=self.global_config['COLOR_BG_HUD']['value']
			credit_surface=font.render(
				msgs[msg_idx],1,
				fg_hud,
				bg_hud 
			)	
			cs_w=credit_surface.get_size()[0]
			cs_h=credit_surface.get_size()[1]
			self.screen.blit(credit_surface,(self.global_config['WIN_W']['value']/2.-cs_w/2.,y0+msg_idx*linesize[1]))

	def go_splash(self):
	
		self.ytop=self.global_config['WIN_H']['value']/2-20
		
		#here we just adjust ytop for possible highscore list below appname:
		dy=10#space btw appname and highscore list
		if self.global_config['DISPLAY_HIGH_SCORES']['value']==1:
			if len(self.global_config['HIGH_SCORES'])>0:
				highscore_string="High Score %02d: %s %d"%(0,self.global_config['HIGH_SCORES'][0][0],self.global_config['HIGH_SCORES'][0][1])
				test_surface=self.hudfont.render(highscore_string,1,self.global_config['COLOR_FG']['value'],self.global_config['COLOR_BG']['value'])
				surf_height=test_surface.get_height()
				self.ytop-=max(len(self.global_config['HIGH_SCORES'])*surf_height,0)
		
		self.screen.fill((0,0,0))
		fg_hud=self.global_config['COLOR_FG']['value']
		bg_hud=self.global_config['COLOR_BG']['value']
		#self.screen.fill(self.global_config['COLOR_BG']['value'])

		self.fwoverlay=FWOverlay(
			self.screen,
			self.global_config['FIREWORKS_DT']['value'],
			self.global_config['FIREWORKS_DT_LAUNCH']['value'],
			self.global_config['FIREWORKS_SCALEFACTOR']['value']
		)
		
		self.STOP_RUNNING=0
		
		self.helpstring="Help:F9"
		hsurf=self.cfont.render(self.helpstring,1,self.global_config['COLOR_BG_BUTTON']['value'],(0,0,0))
		hsurf.set_colorkey(self.global_config['COLOR_BG']['value'])
		H0=self.global_config['WIN_H']['value']-50
		xhelp=self.global_config['WIN_W']['value']-self.admin_button.get_width()/2-50
		yhelp=self.global_config['WIN_H']['value']-self.admin_button.get_height()/2-H0+80
		
		count=0
		while True:
			
			if not len(self.fwoverlay.projectiles):
				if self.SCREENSAVER:
					self.fwoverlay.make_volley(self.global_config['FIREWORKS_SETSIZE']['value'])
			
			if self.STOP_RUNNING!=0:
				#self.onexit()
				#print 'returning ',self.MODE
				return(self.MODE,self.AMFULLSCREEN)
			
			if not self.global_config['SCREENSAVER_ON_AT_START']['value']:
				if time.time()-self.t_last<0.5:
					time.sleep(.1)
					continue
				self.t_last=time.time()

			self.handle_mouse()
			self.handle_keyboard()
			for event in pygame.event.get(KEYDOWN):
				
				if event.key == K_ESCAPE:
					#pygame.quit()
					#sys.exit()
					self.MODE-=1
					self.STOP_RUNNING=1
					return
				
				elif event.key==K_F9:
					self.go_help()
				
				elif event.key==K_F10:
					self.go_credit()
					
				elif event.key ==K_F12:
					pygame.display.toggle_fullscreen()
					self.AMFULLSCREEN*=-1
					
				elif event.key==K_F11:
					try:self.take_screenshot()
					except:pass
			
			pygame.event.clear()
			
			self.screen.fill((0,0,0))
			self.fwoverlay.tick()

			if self.MODE==0:
				self.adminbuttons.draw(self.screen)
				self.screen.blit(hsurf,(xhelp,yhelp))
				
			ytop=self.ytop
			
			pws=self.appnamefont.render('MultiplicationStation',1,bg_hud,(0,0,0))
			pws_w=pws.get_size()[0]
			pws_h=pws.get_size()[1]
			self.screen.blit(pws,(self.global_config['WIN_W']['value']/2.-pws_w/2,ytop))
			ytop+=pws_h
			
			surf=self.hudfont.render('AsymptopiaSoftware | Software@theLimit',1,(255,255,255),(0,0,0))
			surf_w=surf.get_size()[0]
			surf_h=surf.get_size()[1]
			self.screen.blit(surf,(self.global_config['WIN_W']['value']/2.-surf_w/2,ytop))
			ytop+=surf_h
			
			surf=self.hudfont.render('www.asymptopia.org',1,(255,255,255),(0,0,0))
			surf_w=surf.get_size()[0]
			surf_h=surf.get_size()[1]
			self.screen.blit(surf,(self.global_config['WIN_W']['value']/2.-surf_w/2,ytop))
			ytop+=surf_h

			

			pygame.display.flip()
			
	def go_screenshot(self):
		display_surface=pygame.display.get_surface()
		tstamp=self.mktstamp()
		oufname="MultiplicationStation_%s.bmp"%(tstamp)
		try:
			oufname=os.path.join(os.environ['HOME'],oufname)
		except Exception,e:
			if DEBUG:print `e`
		
		pygame.image.save(display_surface,oufname)

	def go_fullscreen(self):
		self.AMFULLSCREEN=pygame.display.toggle_fullscreen()
		if DEBUG:print 'self.AMFULLSCREEN=',self.AMFULLSCREEN

	def on_exit(self):
		lines=[
			'',
			'**********************************************************',
			'*                                                        *',
			'*   You are using version 0.6.2 from January 17, 2010    *',
			'*                                                        *',
			'*                http://www.asymptopia.org               *',
			'*                                                        *',
			'*         AsymptopiaSoftware | Software@theLimit         *',
			'*                                                        *',
			'**********************************************************',
			'',
		]
		
		for line in lines:print line
		pygame.quit()
		sys.exit()
