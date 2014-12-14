#! /usr/bin/python
########################################################################
# GUI for Hackbox Setup
# Copyright (C) 2014  Carl J Smith
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
import json, os, sys, re
# make sure the program is being ran as root
if os.geteuid() != 0:
	print ('gksu "python '+re.sub(' ','\ ',str(os.path.abspath(__file__)))+' '+(' '.join(sys.argv[1:]))+'"')
	os.system('gksu "python '+re.sub(' ','\ ',str(os.path.abspath(__file__)))+' '+(' '.join(sys.argv[1:]))+'"')
	exit()
# launch the program on xterm , make launch in term if in a tty
if os.path.exists('/usr/bin/xterm') == False:#REMOVE WHEN NEW GUI IS BUILT
	os.system('gksu "apt-get install xterm --assume-yes"')#REMOVE WHEN NEW GUI IS BUILT

os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')#REMOVE WHEN NEW GUI IS BUILT
exit()#REMOVE WHEN NEW GUI IS BUILT

try:
	import Tkinter, tkMessageBox
except:
	os.system('gksu "apt-get install python-tk --assume-yes"')
	import Tkinter, tkMessageBox
########################################################################
#text formating command globals
resetTextStyle='\033[0m'
boldtext='\033[1m'
blinktext='\033[5m'
#textcolors
blacktext = '\033[30m'
redtext= '\033[31m'
greentext= '\033[32m'
yellowtext= '\033[33m'
bluetext= '\033[34m'
magentatext= '\033[35m'
cyantext= '\033[36m'
whitetext= '\033[37m'
#background colors
blackbackground= '\033[40m'
redbackground= '\033[41m'
greenbackground= '\033[42m'
yellowbackground= '\033[43m'
bluebackground= '\033[44m'
magentabackground= '\033[45m'
cyanbackground= '\033[46m'
whitebackground= '\033[47m'
########################################################################
# below commands initiate the main tk window then hide it
# this keeps it from popping up behind the pop-ups
rootWindow = Tkinter.Tk()
rootWindow.option_add('*Dialog.msg.width', 40)
rootWindow.withdraw()
########################################################################
def loadFile(fileName):
	try:
		print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	print "Finished Loading :",fileName
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return fail
	return False
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def askQuestion(WindowTitle,WindowText):
	tempAnwser = tkMessageBox.askquestion(WindowTitle,WindowText)
	if tempAnwser == 'yes':
		return 'y'
	else:
		return 'n'
########################################################################
def currentDirectory():
	currentDirectory = os.path.abspath(__file__)
	temp = currentDirectory.split(os.path.sep)
	currentDirectory = ''
	for item in range((len(temp)-1)):
		if len(temp[item]) != 0:
			currentDirectory += os.path.sep+temp[item]
	return (currentDirectory+os.path.sep)
########################################################################
def createInstallLoad():
	# check if a payload has already been built
	if os.path.exists('/etc/hackbox/payload.source'):
		if ('--force-use-config' in sys.argv):
			# install the already created config if force config is used
			installSourcesFile('/etc/hackbox/payload.source')
			return True
		else:
			# otherwise ask the user if they want to use it
			print 'A config already exists, would you like to use it?'
			useConfig = askQuestion('Hackbox Setup','A config already exists, would you like to use it?')
			if useConfig == 'y':
				# end all tk instances, close the window so it dont hang open while xterm is running
				rootWindow.destroy()
				# run the gui install process
				os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')#REMOVE WHEN NEW GUI IS BUILT
				exit()
				return True
			elif useConfig == 'n':
				os.system('rm -rvf /etc/hackbox/*')
	# create a payload variables to orgnize catagories
	payload = ''
	# catagory for ppas and repos
	repoPayload = ''
	# payload for interactive catagory
	interactivePayload = ''
	# payload for things to run first that dont require user interaction
	prePayload = ''
	# add a message to the begining of the pre section since this is the begining of the automated section
	prePayload += 'pre<:>message<:>##################################################################\n'
	prePayload += 'pre<:>message<:>### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###\n'
	prePayload += 'pre<:>message<:>##################################################################\n'
	prePayload += 'pre<:>message<:>### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###\n'
	prePayload += 'pre<:>message<:>##################################################################\n'
	prePayload += 'pre<:>message<:>### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###\n'
	prePayload += 'pre<:>message<:>##################################################################\n'
	prePayload += 'pre<:>message<:>### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###\n'
	prePayload += 'pre<:>message<:>##################################################################\n'
	# main payload where you should put 99% of things
	mainPayload = ''
	# post payload for stuff you should do last
	postPayload = ''
	# read list of datafiles
	datafiles = os.listdir('sources/')
	# sort the files
	datafiles.sort()
	for fileName in datafiles:
		# extract any preconfigured launchers included for this section
		try:
			zipfile.ZipFile(os.path.join(currentDirectory(),('/opt/hackbox/preconfiguredSettings/launchers/'+fileName.split('.')[0]+'.zip'))).extractall('/usr/share/applications')
		except:
			print ('ERROR: File extraction failed for preconfiguredSettings/launchers/'+fileName.split('.')[0]+'.zip')
		# set the install section here to keep it in the scope of the file	
		installSection = 'n'
		# open the .source file
		fileObject = loadFile(os.path.join('sources',fileName))
		if fileObject == False:
			print 'ERROR: Source file',fileName,'does not exist!'
		else:
			fileObject = fileObject.split('\n')
		# clear the screen before loading stuff in this file
		os.system('clear')
		# go though each line of the file
		for line in fileObject:
			# all lines starting with # are comments
			if line[:13]=='#AUTO-INSTALL':
				# skip the question
				installSection = 'y'
			elif line[:6]=='#INFO:':
				# print the info
				print line[6:]
			elif line[:10]=='#QUESTION:':
				# check for install confrimation
				if installSection != 'y':# if the AUTO-INSTALL is not set
					installSection = askQuestion('HackBox Setup',line[10:])
			# run sections if install is set to true for a file
			if line[:1] != '#' and line.find('<:>') != -1 and installSection == 'y':
				# catagories used to orignize the install order of packages
				tempInfo = line.split('<:>')
				if tempInfo[1] == 'deb-repo':
					repoPayload+= line+'\n'
				if tempInfo[1] == 'ppa':
					repoPayload += line+'\n'
				elif tempInfo[0] == 'interactive':
					interactivePayload += line+'\n'
				elif tempInfo[0] == 'pre':
					prePayload += line+'\n'
				elif tempInfo[0] == 'main':
					mainPayload += line+'\n'
				elif tempInfo[0] == 'post':
					postPayload += line+'\n'
				else:
					# otherwise add uncatagorized payloads to main payload
					mainPayload += line+'\n'	
	repoPayload += 'null<:>command<:>apt-get update\n'
	# orginize the payload contents
	payload = repoPayload+interactivePayload+prePayload+mainPayload+postPayload
	# write the payload to a text file
	writeFile('/etc/hackbox/payload.source',payload)
	# return the payload file location
	return '/etc/hackbox/payload.source'
########################################################################
os.chdir(currentDirectory())
# create the install load
createInstallLoad()
# end all tk instances, close the window so it dont hang open while xterm is running
rootWindow.destroy()
# run the gui install process
os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')#REMOVE WHEN NEW GUI IS BUILT
# exit the program at the end of the install procedure
exit()


########################################################################
# more globals, config data is the meat of the program here
configData = {}
# create variable for figuring progress of this process
totalSections=0;
########################################################################
# make sure the program is being ran as root
if os.geteuid() != 0:
	print ('gksu "python '+re.sub(' ','\ ',str(os.path.abspath(__file__)))+' '+(' '.join(sys.argv[1:]))+'"')
	os.system('gksu "python '+re.sub(' ','\ ',str(os.path.abspath(__file__)))+' '+(' '.join(sys.argv[1:]))+'"')
	exit()
# set the background if in fullscreen
os.system('xterm -e fbsetbg /opt/hackbox/media/wallpapers/hackboxWallpaperBranded.png')
# set current directory to be same as this file
os.chdir(currentDirectory())
# check for config file
if os.path.exists('hackBox.conf'):
	loadConfigFile = askQuestion('1/20','Config file detected! Would you like to use it?')
	if loadConfigFile == 'y':
		configData = json.loads(loadFile('hackBox.conf'))
		# check if all data is in the config file, if not rebuild one
		try:
			print (configData['systemTools']+configData['officeSoftware']+configData['graphicsTools']+configData['soundAndVideoTools']+configData['webDesignTools']+configData['programmingTools']+configData['gamesAndEmulation']+configData['steamGames']+configData['customSettingsCheck']+configData['customSettingsCheckLogout']+configData['restrictedExtras']+configData['webcamCheck']+configData['redShiftCheck']+configData['netflix']+configData['rebootCheck'])
		except:
			print 'ERROR: Config file not compatible or corrupted!'
			configData = {}
	else:
		configData = {}
if configData == {}:
	# Section for basic software / security needs
	configData['basicSoftwareAndSecurity'] = 'y'
	# system tools section
	configData['systemTools'] = askQuestion('System Tools? 4/20','Would you like to install System tools?')
	# Section for office software
	configData['officeSoftware'] = askQuestion('4/20','Would you like to install Office Software?')
	# Section for graphics software
	configData['graphicsTools'] = askQuestion('5/20','Would you like to install Graphics Tools?')
	# sound and video
	configData['soundAndVideoTools'] = askQuestion('6/20','Would you like to install Sound and Video Tools?')
	# web design tools
	configData['webDesignTools'] = askQuestion('7/20','Would you like to install Web Design Tools?')
	# section for programming tools
	configData['programmingTools'] = askQuestion('8/20','Would you like to install Programming Tools?')
	# Games & Emulation / Other Shit
	configData['gamesAndEmulation'] = askQuestion('9/20','Would you like to install games and emulation software?')
	if configData['gamesAndEmulation'] == 'y':
		configData['steamGames'] = askQuestion('','Would you like to install the Steam Client?')
	else:
		configData['steamGames'] = 'n'
	# runs unattended upgrade and saves session with all open programs which
	# will make any open programs run on next login at startup
	# Check before proceeding with section if user wants it configured
	##configData['autoUpdates'] = askQuestion('10/20','Would you like to install and configure automatic updates?')
	# dont ask the user just install automatic updates 
	configData['autoUpdates'] = 'y' 
	# custom desktop setup
	configData['customSettingsCheck'] = askQuestion('11/20',('Do you want to configure the custom desktop setup for the current user?\n\n'+'This is recommended if you are on a fresh install, '+'HOWEVER'+' it is not recommended if you have transfered your settings from a old system or have already configured things in a way you like.'))
	if configData['customSettingsCheck'] == 'y':
		# this sets up a different default desktop
		configData['bottomBar'] = askQuestion('12/20','Do you want the bar on the bottom(e.g. like windows)?')
	else:
		configData['bottomBar'] = askQuestion('12/20','Do you want the bar on the bottom for newly created users(e.g. like windows)?')
	# check to see if the user would like to logout to refresh their settings
	if configData['customSettingsCheck'] == 'y' and (('--no-reset' in sys.argv) != True):
		configData['customSettingsCheckLogout'] = askQuestion('12.1/20','Would you like to logout at the end of the script to enable your new settings?')
	else:
		configData['customSettingsCheckLogout'] = 'n'
	# Installs flash and all of Ubuntu's restricted codecs
	# the following commands install libdvdcss which allows DVD playback on Ubuntu
	configData['restrictedExtras'] = askQuestion('13/20','Would you like to install DVD support and the Restricted Extras for your PC?\n\nThis means codecs, Flashplayer, etc.')
	# Webcam Check
	configData['webcamCheck'] = askQuestion('14/20','Do you have a webcam?')
	# check if the user would like to install redshift
	configData['redShiftCheck'] = askQuestion('15/20','Would you like to install Redshift?\n\n(A program that adjusts monitor color throughout the day to reduce eye strain?)')
	# check if the user would like to install netflix
	configData['netflix'] = askQuestion('16/20','Would you like to install Netflix?\n\nA desktop program that lets you run Netflix on Linux?')
	if configData['customSettingsCheckLogout'] == 'n':
		# check if the user would like to reboot after install
		configData['rebootCheck'] = askQuestion('17/20','Would you like to reboot the system after install is complete?\n\n(This is recommended, but not always necessary)')
	else:
		configData['rebootCheck'] = 'n'
	#~ # check if user would like to donate though the affiliate program
	#~ configData['affilateCheck'] = askQuestion('18/20',('Do you want to passively donate to the continuation of the project though using our Firefox extension?\n\n'+'This will not give us any of your personal info, it will only apply our affiliate tag to purchases though certain websites.\n\n'+'This will '+'NOT'+' charge you any money!'))
	# Save Settings
	if os.path.exists('hackbox.conf'):
		configSaveCheck = askQuestion('19/20','Would you like to save this configuration for next time?')
	else:
		# if user has no previous config the current settings will be saved to a config
		# this is because the GUI requires a config to be saved to launch the main program
		configSaveCheck = 'y'
	if configSaveCheck == 'y':
		writeFile(os.path.abspath('hackBox.conf'),json.dumps(configData))
	for index in configData:
		if configData[index] == 'y':
			totalSections += 1
	########################################################################
	if totalSections == 0:
		tkMessageBox.showinfo('Nothing to do!','Nothing to be installed or configured. Ending Program...')
		exit();
	########################################################################
def formatAnwser(anwser):
	if anwser == 'y':
		return ('True')
	else:
		return ('False')
if totalSections == 0:
	for index in configData:
		if configData[index] == 'y':
			totalSections += 1
settingsScreen = ''
settingsScreen += 'Total Sections to Install = ' + str(totalSections) + '\n\n'
settingsScreen += 'Setup Basic Tools & Security = ' + formatAnwser(configData['basicSoftwareAndSecurity']) + '\n'
settingsScreen += 'System Tools = ' + formatAnwser(configData['systemTools']) + '\n'
settingsScreen += 'Office Software = ' + formatAnwser(configData['officeSoftware']) + '\n'
settingsScreen += 'Graphics Software = ' + formatAnwser(configData['graphicsTools']) + '\n'
settingsScreen += 'Sound and Video Tools= ' + formatAnwser(configData['soundAndVideoTools']) + '\n'
settingsScreen += 'WebDesign Tools = ' + formatAnwser(configData['webDesignTools']) + '\n'
settingsScreen += 'Programming Tools = ' + formatAnwser(configData['programmingTools']) + '\n'
settingsScreen += 'games/emulation/other = ' + formatAnwser(configData['gamesAndEmulation']) + '\n'
settingsScreen += 'Setup Webcam Support = ' + formatAnwser(configData['webcamCheck']) + '\n'
settingsScreen += 'Setup DVD/Flash Support = ' + formatAnwser(configData['restrictedExtras']) + '\n'
settingsScreen += 'Enable Automatic Updates = ' + formatAnwser(configData['autoUpdates']) + '\n'
settingsScreen += 'Install Redshift =' + formatAnwser(configData['redShiftCheck']) + '\n'
settingsScreen += 'Reboot after install =' + formatAnwser(configData['rebootCheck']) + '\n'
#~ settingsScreen += 'Passively Donate = ' + formatAnwser(configData['affilateCheck']) + '\n'
settingsScreen += 'Custom Desktop Config = ' + formatAnwser(configData['customSettingsCheck']) + '\n'
settingsScreen += 'Netflix Desktop = ' + formatAnwser(configData['netflix']) + '\n\n'
# prompt user if they want to proceed or not
settingsScreen += 'Are the above settings correct?';
check = askQuestion('FINAL CHECK 20/20',settingsScreen)
# end all tk instances, close the window so it dont hang open while xterm is running
rootWindow.destroy()
print sys.argv
if check == 'y' :
	if os.path.exists('/usr/bin/xterm') == False:
		os.system('gksu "apt-get install xterm --assume-yes"')
	print 'Starting setup...';
	if '--no-reset' in sys.argv:
		#os.system('xterm -maximized -T Hackbox\ Setup -e "python hackboxsetup.py --force-use-config --no-reset"')
		os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')
	else:
		#os.system('xterm -maximized -T Hackbox\ Setup -e "python hackboxsetup.py --force-use-config"')
		os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')

	if '--runonce' in sys.argv:
		os.system('rm -v /etc/xdg/autostart/hackboxRunonce.desktop')
else:
	print 'Ending script...';
	exit();
