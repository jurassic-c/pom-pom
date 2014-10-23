#!/usr/bin/python

import appindicator
import pynotify
import gtk
from datetime import datetime, timedelta
from time import sleep
import gobject
import pygame

a = appindicator.Indicator('pompom_indicator', '/home/coaltown/projects/current/PomPom/icon.png', appindicator.CATEGORY_APPLICATION_STATUS)
a.set_status( appindicator.STATUS_ACTIVE )
a.set_label("00:00")
m = gtk.Menu()
start_btn = gtk.MenuItem( 'Start' )
pause_btn = gtk.MenuItem( 'Pause' )
qi = gtk.MenuItem( 'Quit' )

m.append(start_btn)
m.append(pause_btn)
m.append(qi)

a.set_menu(m)
start_btn.show()
pause_btn.show()
qi.show()

tomatoes = 0
current_tomato = {"start": None, "last_pause": None, "mode": "work", "paused": True, "pause_offset": timedelta()}

pynotify.init("PomPom")
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("/home/coaltown/projects/current/PomPom/alarm.mp3")

def start(item):
	global start_btn_connect
	a.set_icon('/home/coaltown/projects/current/PomPom/icon-task-running.png')
	current_tomato["paused"] = False
	current_tomato["start"] = datetime.now()
	start_btn.set_label("Stop")
	start_btn.disconnect(start_btn_connect)
	start_btn_connect = start_btn.connect('activate', stop)
	update_time()
	n = pynotify.Notification("PomPom", "New Pomodoro Started")
	n.show()

def update_time():
	global tomatoes
	mins = 0
	secs = 0
	if current_tomato["paused"] == False:
		if current_tomato["start"] == None:
			current_tomato["start"] = datetime.now()
			current_tomato["pause_offset"] = timedelta()
		now = datetime.now()
		delta = now - current_tomato["start"] - current_tomato["pause_offset"]
		if current_tomato["mode"] == "work":
			seconds = (25*60)-delta.seconds
			if seconds <= 0:
				seconds = 0
				current_tomato["mode"] = "break"
				current_tomato["start"] = None
				if (tomatoes+1) % 4:
					n = pynotify.Notification("PomPom", "Work time is over. Take a break!")
					pygame.mixer.music.play()
					gobject.timeout_add(3000, stop_alarm)
					n.show()
				else:
					n = pynotify.Notification("PomPom", "Work time is over. Take a nice long break!")
					pygame.mixer.music.play()
					gobject.timeout_add(3000, stop_alarm)
					n.show()
				a.set_icon('/home/coaltown/projects/current/PomPom/icon-break-running.png')
		elif current_tomato["mode"] == "break":
			if(tomatoes+1) % 4:
				seconds = (5*60)-delta.seconds
			else:
				seconds = (15*60)-delta.seconds
			if seconds <= 0:
				seconds = 0
				current_tomato["mode"] = "work"
				current_tomato["start"] = None
				n = pynotify.Notification("PomPom", "Break is over. Get to work!")
				n.show()
				a.set_icon('/home/coaltown/projects/current/PomPom/icon-task-running.png')
				pygame.mixer.music.play()
				gobject.timeout_add(3000, stop_alarm)
				tomatoes+= 1
		mins = str(seconds / 60).rjust(2, "0")
		secs = str(seconds % 60).rjust(2, "0")
		a.set_label("%s: %s:%s" % (tomatoes+1, mins, secs))
	gobject.timeout_add(1000, update_time)

def stop_alarm():
	pygame.mixer.music.stop()

def pause(item):
	if current_tomato["paused"]:
		current_tomato["paused"] = False
		current_tomato["pause_offset"]+= (datetime.now() - current_tomato["last_pause"])
		if current_tomato["mode"] == "work":
			a.set_icon('/home/coaltown/projects/current/PomPom/icon-task-running.png')
		else:
			a.set_icon('/home/coaltown/projects/current/PomPom/icon-break-running.png')
	else:
		current_tomato["last_pause"] = datetime.now()
		current_tomato["paused"] = True
		if current_tomato["mode"] == "work":
			a.set_icon('/home/coaltown/projects/current/PomPom/icon-task-pause.png')
		else:
			a.set_icon('/home/coaltown/projects/current/PomPom/icon-break-pause.png')

def stop(item):
	global start_btn_connect
	a.set_icon('/home/coaltown/projects/current/PomPom/icon.png')
	start_btn.set_label("Start")
	start_btn.disconnect(start_btn_connect)
	start_btn_connect = start_btn.connect('activate', start)
	current_tomato["paused"] = True
	a.set_label("%s: 00:00" % tomatoes)

def quit(item):
        gtk.main_quit()

start_btn_connect = start_btn.connect('activate', start)
pause_btn.connect('activate', pause)
qi.connect('activate', quit)

gtk.main()
