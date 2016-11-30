#! /usr/bin/python
########################################################################
# GUI components of HackBox to interface with the user
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
# INDEX
# - progressBar()
# - dialogProgressBar()
# - textProgressBar()
# - askQuestion()
# - textQuestion()
# - cursedDialogQuestion()
########################################################################
import os, sys
sys.path.append('/opt/hackbox/')
import hackboxlib
########################################################################
# Activate the gui object if possible
try:
	#from dialog import Dialog
	import dialog
	queryboxes = dialog.Dialog()
except:
	hackboxlib.logMessage('ERROR : Curses dialog did not work!')
########################################################################
def cursesDialogQuestion(questionText):
	'''
	Display a question with a curses interface and return 'y' or 'n' string.
	'''
	# returns 0 for yes and 1 for no
	if queryboxes.yesno(questionText)=='ok':
		anwser = 'y'
	else:
		anwser = 'n'
	return anwser
########################################################################
def textQuestion(questionText):
	'''
	Display a question with a text only interface, return a 'y' or 'n'
	string.
	'''
	# use text gui if curses fails
	if os.path.exists('/opt/hackbox/media/banner.txt'):
		banner = hackboxlib.loadFile('/opt/hackbox/media/banner.txt')
		print(hackboxlib.colorText(banner))
	# otherwise ask the user if they want to use it
	print(questionText)
	anwser = input('[y/n]: ')
	return anwser
########################################################################
def askQuestion(questionText):
	'''
	Ask a question using the most graphical interface, while falling back
	upon failure to lower level interfaces.
	'''
	if '--no-curses' in sys.argv:
		# the user supplied no curses so use it no matter what
		anwser = textQuestion(questionText)
	else:
		try:
			# try to use curses dialog first
			anwser = cursesDialogQuestion(questionText)
		except:
			# text question runs as a failsafe
			anwser = textQuestion(questionText)
	return anwser
########################################################################
def dialogProgressBar(percentage,messageText,banner):
	'''
	Draw a dialog progressbar.
	'''
	dialogBar = dialog.Dialog()
	dialogBar.setBackgroundTitle(banner)
	dialogBar.gauge_start(percent=percentage,text=messageText)
	dialogBar.gauge_stop()
########################################################################
def textProgressBar(percentage,messageText,banner,logFile='/opt/hackbox/Install_Log.txt'):
	'''
	Draw a text progress bar.
	'''
	# display progress by clearing the screen and writing the updates
	hackboxlib.clear()
	# draw the banner if the file path exists
	if os.path.exists('/opt/hackbox/media/banner.txt'):
		print(hackboxlib.loadFile('/opt/hackbox/media/banner.txt'))
	barWidth = int(percentage / 2)
	print('='*80)
	print(messageText)
	colorBar=hackboxlib.colorText('<greenbackground> </>')
	print('Total Progress : [' + (colorBar * barWidth) + ((50 - barWidth) * ' ') + '] ' + str(percentage) + '%')
	print('='*80)
	# print the last several lines of output on refresh
	os.system('tail ' + logFile + ' || echo "WARNING : No log found..."')
########################################################################
def progressBar(percentage,messageText,banner,logFile='/opt/hackbox/Install_Log.txt'):
	'''
	Draw a curses based progressbar with the current precentage,
	displaying the messageText below the bar, and the banner text
	being displayed in the top left. Fall back to the text interface
	if curses interface fails.

	:return None
	'''
	percentage=int(percentage)
	messageText=str(messageText)
	if '--no-curses' in sys.argv:
		textProgressBar(percentage,messageText,banner,logFile)
	else:
		# try using dialog
		try:
			dialogProgressBar(percentage,messageText,banner)
		except:
			# log messages
			hackboxlib.logMessage('ERROR : Curses dialog failed!')
			hackboxlib.logMessage('DEBUG : percentage = "'+str(type(percentage))+'", messageText = "'+str(type(messageText))+'", banner = "'+str(type(banner))+'"')
			hackboxlib.logMessage('DEBUG : percentage = "'+str(percentage)+'", messageText = "'+messageText+'", banner = "'+banner+'"')
			# run command again with no curses interface
			textProgressBar(percentage,messageText,banner,logFile)
	return True

