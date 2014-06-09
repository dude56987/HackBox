#! /usr/bin/python
########################################################################
# Program Designed to setup a new Linux system automatically via scripts
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
import os, sys, shutil, json, zipfile, socket, urllib2
########################################################################
Version = '0.5.0'
# For Ubuntu Server Edition/Ubuntu Desktop Edition/Linux Mint
########################################################################
#TODO:
# ~ add some sort of progress indication ~ (Needs Improvement)
# ~ optimize each section into a single os.system call???
# ~ Make entire thing into one payload based on choices
#   variable for each item to install add 1 then / to get percent done
# ~ custom distro???
########################################################################
#text formating command globals
defaultText='\033[0m'
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
# reset to default style
resetTextStyle=defaultText+blackbackground+whitetext
# define functions
########################################################################
def deleteFile(filePath):
	if os.path.exists(filePath):
		os.remove(filePath)
		return True
	else:
		print "ERROR: file does not exist, so can not remove it."
		return False
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
def downloadFile(fileAddress):
	try:
		print "Downloading :",fileAddress
		downloadedFileObject = urllib2.urlopen(str(fileAddress))
	except:
		print "Failed to download :",fileAddress
		return "FAIL"
	lineCount = 0
	fileText = ''
	for line in downloadedFileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount+=1
	downloadedFileObject.close()
	print "Finished Loading :",fileAddress
	return fileText
########################################################################
def replaceLineInFile(fileName,stringToSearchForInLine,replacementText):
	# open file
	temp = loadFile(fileName)
	# if file exists append, if not write
	newFileText = ''
	if temp != False:
		temp = temp.split('\n')
		for line in temp:
			if line.find(stringToSearchForInLine) == -1:
				newFileText += line+'\n'
			else:
				if replacementText != '':
					print 'Replacing line:',line
					print 'With:',replacementText
					newFileText += replacementText+'\n'
				else:
					print 'Deleting line:',line
	else:
		return False
	writeFile(fileName,newFileText)
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
def makeDir(remoteDir):
	import os
	''' Creates the defined directory, if a list of directories are listed
	that do not exist then they will be created as well, so beware of 
	spelling mistakes as this will create the specified directory you 
	type mindlessly.'''
	temp = remoteDir.split('/')
	remoteDir= ''
	for i in temp:
		remoteDir += (i + '/')
		if os.path.exists(remoteDir):
			print remoteDir , ': Already exists!, Moving on...'
		else:
				os.mkdir(remoteDir)
########################################################################
def replaceLineInFileOnce(fileName,StringToSearchFor,StringToReplaceWith):
	'''Takes a file and replaces a string in it with a new one, the 
	function checks to that it wont dupe the replacements'''
	# run a replace in case the string already exists
	text = loadFile(fileName).replace(StringToReplaceWith,StringToSearchFor)
	# then replace the string so there are no dupes
	text = text.replace(StringToSearchFor,StringToReplaceWith)
	return writeFile(fileName,text)
########################################################################
def clear():
	os.system('clear');
########################################################################
def printBlue(text):
	temp = bluetext+boldtext+text+resetTextStyle
	print temp
########################################################################
def printGreen(text):
	temp = greentext+boldtext+text+resetTextStyle
	print temp
########################################################################
def COPY(src,dest):
	'''Copies a directory recursively from the "src" to the "dest"'''
	if src.split('/')[len(src.split('/'))-1].find('.') > -1:
		# this is a single file being copied to a directory so use shutil.copy
		if os.path.exists(src):
			if os.path.exists(dest):
				shutil.copy(src,dest)
				return True
			else:
				return False
		else:
			return False
	else:
	# this is for a directory of files being copied to another directory
		try:
			if os.path.exists(src):
				if os.path.exists(dest):
					# if dest path already exists throw a error and do not overwrite
					print 'ERROR:',dest,'Already Exists, Will not Overwrite!'
					return False
				else:
					shutil.copytree(src,dest)
					return True
			else:
				#if src path does not exist throw a error and do not overwrite
				print 'ERROR:',src,'Does Not Exist!'
				return False
		except:
			print 'ERROR: a unknown error occurred when copying',src,'to',dest
			return False
########################################################################
def installSourcesFile(fileNameOfFile):
	'''Reads a source file of programs to install and installs them.'''
	# change this so that source files are split into 3 pieces of data
	# first the type of data, second the message to print, third the data
	# itself, the data would depend on the data type described in the first
	# space of the line
	packageManager=False
	if os.path.exists('/usr/bin/apt-get'):
		packageManager = 'apt-get'
	if os.path.exists('/usr/sbin/apt-fast'):
		packageManager = 'apt-fast'
	if packageManager == False:
		return False
	fileObject = loadFile(fileNameOfFile)
	if fileObject == False:
		print 'ERROR: Source file',fileNameOfFile,'does not exist!'
		return False
	else:
		fileObject = fileObject.split('\n')
	# go though each line of the file
	for line in fileObject:
		# all lines starting with # are comments	
		if line[:1] != '#':
			if line.find('<:>') != -1:
				# example format of file
				# subcatagory<:>type<:>data
				# types are command, package, and message
				# command will execute a bash command
				# package requireds a extra component
				# subcatagory<:>package<:>packageName
				tempInfo = line.split('<:>')
				if tempInfo[1] == 'message':
					printGreen(tempInfo[2]+'...')
				elif tempInfo[1] == 'command':
					# execute command
					print tempInfo[2]
					os.system(tempInfo[2])
				elif tempInfo[1] == 'package':
					#/usr/share/doc/packagename is checked to see if the package has already been installed
					# install package
					if (os.path.exists('/usr/share/doc/'+tempInfo[2]) != True):
						os.system((packageManager+' install '+tempInfo[2]+' --assume-yes >> Install_Log.txt'))
	return True
########################################################################
# Pre-run checks
print 'Preforming startup checks...'
# run program as root if it is not being already done
if os.geteuid() != 0:
	if len(sys.argv) > 1:
		os.system('sudo python '+(os.path.abspath(__file__))+' '+sys.argv[1])
	else:
		os.system('sudo python '+(os.path.abspath(__file__)))
	exit()
# set current directory to be same as this file
os.chdir(currentDirectory())
# banner to show the program
clear()
banner  =bluetext
banner +='/#########################################################\\'+'\n'
banner +='\\############## '
banner +=whitetext+boldtext+'HackBox Setup Script v'+Version+resetTextStyle
banner +=bluetext+' ##############/'+'\n'
banner +=' \\#######################################################/'+'\n'
banner +=resetTextStyle


print banner
print 'Designed for:'+greentext+'Ubuntu Desktop Edition/Linux Mint Xfce Edition'+resetTextStyle
if os.geteuid() == 0:
	print 'Running as root : '+greentext+'YES'+resetTextStyle
else:
	print 'Running as root : '+redtext+'NO'+resetTextStyle
# only prompt the user if --force-use-config is not used in the program launch
if (('--force-use-config' in sys.argv) == False):
	# prompt user if they want to proceed or not
	printBlue('This script will install and configure settings for a new \n system automatically.');
	check = raw_input('Proceed? [y/n]: ');
	if check == 'y' :
		print 'Starting setup...';
	else:
		clear();
		print 'Ending script...';
		exit();

# sets all following commands to root user control
print 'This program requires your password to proceed. Please input your password.'
os.system("echo 'Program will now proceed...'");
########################################################################
# Check all of the software before any tasks starts to see which sets
# the user wants to install, and which special checklist items the user
# wants
########################################################################
clear();
os.chdir(currentDirectory())
# check for config file
configData = {}
# things that are installed by default
configData['basicSoftwareAndSecurity'] = 'y'
configData['autoUpdates'] = 'y'
if os.path.exists('hackBox.conf'):
	if (('--force-use-config' in sys.argv) == False):
		printBlue('Config file detected! Would you like to use it?')
		loadConfigFile = raw_input('[y/n]: ');
	else:
		loadConfigFile = 'y'
	if loadConfigFile == 'y':
		configData = json.loads(loadFile('hackBox.conf'))
		# check if all data is in the config file, if not rebuild one
		try:
			print 'Checking config file for compatibility...'
			print (configData['updateCheck']+configData['systemTools']+configData['officeSoftware']+configData['graphicsTools']+configData['soundAndVideoTools']+configData['webDesignTools']+configData['programmingTools']+configData['gamesAndEmulation']+configData['steamGames']+configData['autoUpdates']+configData['customSettingsCheck']+configData['customSettingsCheckLogout']+configData['restrictedExtras']+configData['webcamCheck']+configData['redShiftCheck']+configData['netflix']+configData['rebootCheck'])
		except:
			print 'ERROR: Config file not compatible or corrupted!'
			configData = {}
	else:
		configData = {}
if configData == {}:
	# create variable for figuring progress of this process
	totalSections=0;
	#~ # Section for base system setup
	#~ print banner
	#~ printBlue('Would you like to install the Base System?');
	#~ printBlue('This is for installing from a bare cli linux system.');
	#~ configData['baseSystemCheck'] = raw_input('[y/n]: ');
	#~ if configData['baseSystemCheck'] == 'y':
		#~ totalSections += 1;
	#~ clear();
	# check if the user wants to upgrade before start
	clear()
	print banner
	printBlue('Do you want to upgrade all current software before install?(This is highly recommended)')
	configData['updateCheck'] = raw_input('[y/n]: ');
	if configData['updateCheck'] == 'y':
		totalSections += 1;
	clear();
	# system tools section
	print banner
	printBlue('Would you like to install System tools?');
	configData['systemTools'] = raw_input('[y/n]: ');
	if configData['systemTools'] == 'y':
		totalSections += 1;
	clear();
	# Section for office software
	print banner
	printBlue('Would you like to install Office Software?');
	configData['officeSoftware'] = raw_input('[y/n]: ');
	if configData['officeSoftware'] == 'y':
		totalSections += 1;
	clear();
	# Section for graphics software
	print banner
	printBlue('Would you like to install Graphics Tools?');
	configData['graphicsTools'] = raw_input('[y/n]: ');
	if configData['graphicsTools'] == 'y':
		totalSections += 1;
	clear();
	# sound and video
	print banner
	printBlue('Would you like to install Sound and Video Tools?');
	configData['soundAndVideoTools'] = raw_input('[y/n]: ');
	if configData['soundAndVideoTools'] == 'y':
		totalSections += 1;
	clear();
	# web design tools
	print banner
	printBlue('Would you like to install Web Design Tools?');
	configData['webDesignTools'] = raw_input('[y/n]: ');
	if configData['webDesignTools'] == 'y':
		totalSections += 1;
	clear();
	# section for programming tools
	print banner
	printBlue('Would you like to install Programming Tools?');
	configData['programmingTools'] = raw_input('[y/n]: ');
	if configData['programmingTools'] == 'y':
		totalSections += 1;
	clear();
	# Games & Emulation / Other Shit
	print banner
	printBlue('Would you like to install games and emulation software?');
	configData['gamesAndEmulation'] = raw_input('[y/n]: ');
	if configData['gamesAndEmulation'] == 'y':
		printBlue('Would you like to install the Steam Client?')
		configData['steamGames'] = raw_input('[y/n]: ');
		totalSections += 1;
	else:
		configData['steamGames'] = 'n'
	clear();
	# custom desktop setup
	print banner
	printBlue('Do you want to configure the custom desktop setup for the current user?')
	print('This is recommended if you are on a fresh install, '+boldtext+redtext+'HOWEVER'+resetTextStyle+' it is not recommended if you have transfered your settings from a old system or have already configured things in a way you like.')
	configData['customSettingsCheck'] = raw_input('[y/n]: ');
	if configData['customSettingsCheck'] == 'y':
		totalSections += 1;
		# this sets up a different default desktop
		printBlue('Do you want the bar on the bottom(e.g. like windows)?')
		configData['bottomBar'] = raw_input('[y/n]: ');
	else:
		printBlue('Do you want the bar on the bottom for newly created users(e.g. like windows)?')
		configData['bottomBar'] = raw_input('[y/n]: ');
	# logout check
	if configData['customSettingsCheck'] == 'y' and (('--no-reset' in sys.argv) != True):
		printBlue('Would you like to logout at the end of the script to enable your new settings?')
		configData['customSettingsCheckLogout'] = raw_input('[y/n]: ');
	else:
		configData['customSettingsCheckLogout'] = 'n'
	clear();
	# Installs flash and all of Ubuntu's restricted codecs
	# the following commands install libdvdcss which allows dvd playback on Ubuntu
	print banner
	printBlue('Would you like to install DVD support and the \nRestricted Extras for your PC?');
	printBlue('This means codecs, Flashplayer, etc.');
	configData['restrictedExtras'] = raw_input('[y/n]: ');
	if configData['restrictedExtras'] == 'y':
		totalSections += 1;
	clear();
	# Webcam Check
	print banner
	printBlue('Do you have a webcam?');
	configData['webcamCheck'] = raw_input('[y/n]: ');
	if configData['webcamCheck'] == 'y':
		totalSections += 1;
	clear();
	
	# check if the user would like to install redshift
	print banner
	printBlue('Would you like to install Redshift?')
	printBlue('(A program that adjusts monitor color throughout the day to reduce eye strain?')
	configData['redShiftCheck'] = raw_input('[y/n]: ');
	if configData['redShiftCheck'] == 'y':
		totalSections += 1;
	clear()
	# check if the user would like to install Netflix
	print banner
	printBlue('Would you like to install Netflix?')
	printBlue('A desktop program that lets you run Netflix on Linux?')
	configData['netflix'] = raw_input('[y/n]: ');
	if configData['netflix'] == 'y':
		totalSections += 1;
	clear()
	if configData['customSettingsCheckLogout'] == 'n':
		# check if the user would like to reboot after install
		print banner
		printBlue('Would you like to reboot the system after install is complete?')
		printBlue('(This is recommended, but not always necessary)')
		configData['rebootCheck'] = raw_input('[y/n]: ');
		clear()
	else:
		configData['rebootCheck'] = 'n'
	#~ # check if user would like to donate though the affiliate program
	#~ print banner
	#~ printBlue('Do you want to passively donate to the continuation of the project though using our Firefox extension?')
	#~ print('This will not give us any of your personal info, it will only apply our affiliate tag to purchases though certain websites.')
	#~ print ('This will '+boldtext+redtext+'NOT'+resetTextStyle+' charge you any money!')
	#~ configData['affilateCheck'] = raw_input('[y/n]: ');
	#~ if configData['affilateCheck'] == 'y':
		#~ totalSections += 1;
	#~ clear();
	# Save Settings
	print banner
	printBlue('Would you like to save this configuration for next time?');
	configSaveCheck = raw_input('[y/n]: ');
	if configSaveCheck == 'y':
		writeFile(os.path.abspath('hackBox.conf'),json.dumps(configData))
	clear();
	########################################################################
	if totalSections == 0:
		print 'Nothing to be installed or configured. Ending Program...'
		exit();
	########################################################################
	def formatAnwser(anwser):
		if anwser == 'y':
			return (resetTextStyle + greentext + boldtext + 'True' + resetTextStyle)
		else:
			return (resetTextStyle + redtext + boldtext + 'False' + resetTextStyle)
	print banner
	settingsScreen = ''
	settingsScreen += greentext + 'Total Sections to Install = ' + resetTextStyle
	settingsScreen += bluetext + boldtext + str(totalSections) + resetTextStyle + '\n'
	settingsScreen += bluetext+boldtext+('='*60)+resetTextStyle+'\n'
	settingsScreen += 'System Tools = ' + formatAnwser(configData['systemTools']) + '\t\t\t'
	settingsScreen += 'Office Software = ' + formatAnwser(configData['officeSoftware']) + '\n'
	settingsScreen += 'Graphics Software = ' + formatAnwser(configData['graphicsTools']) + '\t\t'
	settingsScreen += 'Sound and Video Tools= ' + formatAnwser(configData['soundAndVideoTools']) + '\n'
	settingsScreen += 'WebDesign Tools = ' + formatAnwser(configData['webDesignTools']) + '\t\t\t'
	settingsScreen += 'Programming Tools = ' + formatAnwser(configData['programmingTools']) + '\n'
	settingsScreen += 'games/emulation/other = ' + formatAnwser(configData['gamesAndEmulation']) + '\t\t'
	settingsScreen += 'Setup Webcam Support = ' + formatAnwser(configData['webcamCheck']) + '\n'
	settingsScreen += 'Setup DVD/Flash Support = ' + formatAnwser(configData['restrictedExtras']) + '\t\t'
	settingsScreen += 'Enable Automatic Updates = ' + formatAnwser(configData['autoUpdates']) + '\n'
	settingsScreen += 'Install Redshift =' + formatAnwser(configData['redShiftCheck']) + '\t\t\t'
	settingsScreen += 'Reboot after install =' + formatAnwser(configData['rebootCheck']) + '\n'
	settingsScreen += 'Upgrade before install = ' + formatAnwser(configData['updateCheck']) + '\t\t'
	settingsScreen += 'Custom Desktop Config = ' + formatAnwser(configData['customSettingsCheck']) + '\n'
	settingsScreen += 'Netflix Desktop = ' + formatAnwser(configData['netflix']) + '\n'
	
	settingsScreen += bluetext+boldtext+('='*60)+resetTextStyle+'\n'
	
	print settingsScreen
	# prompt user if they want to proceed or not
	printBlue('Check if the above settings are correct.');
	check = raw_input('Proceed? [y/n]: ');
	if check == 'y' :
		print 'Starting setup...';
	else:
		clear();
		print 'Ending script...';
		exit();
	clear();
# now (completed/totalSections)*100=Progress in percentage
#exit();# Uncomment for debug
########################################################################
# Start Installing everything
########################################################################
# create the install log
os.system('echo "Starting Install Process..." >> Install_Log.txt');
os.system('echo "Started on ${date}" >> Install_Log.txt');
print '##################################################################'
print '   ___    _   __'
print '  / _ \  (_) / /'
print ' | | | |    / / '
print ' | | | |   / /  '
print ' | |_| |  / / _ '
print '  \___/  /_/ (_)'
print '##################################################################'
########################################################################
# run some commands that will keeps the screen from blanking during install
# these will fail in the terminal but that wont stop the program
os.system('xset s 0 0')
os.system('xset s off')
os.system('xset -dpms')
########################################################################
if configData['autoUpdates'] == 'y':
	print 'Checking for installing automated updates...';
	# remove other update programs from annoying the user
	os.system('apt-fast purge mintupdate --assume-yes')
	os.system('apt-fast purge update-manager --assume-yes')
	os.system('apt-fast purge update-notifier --assume-yes')
	# add update command to computer regardless of user decisions
	os.system('gdebi --no unsupportedPackages/update.deb')
########################################################################
# install things that require user interaction to proceed first
########################################################################
# Games & Emulation / Other Shit (requires user interaction)
# add all ppa's first this will add the software to your repos after you
# update them, none of these items should output to a logfile either
printGreen('Adding additional repos...')
# add getdeb and playdeb repos using the package files they supply
os.system('gdebi unsupportedPackages/getdeb.deb --non-interactive')
os.system('gdebi unsupportedPackages/playdeb.deb --non-interactive')
# cleanup sources, above leaves backup files, other stuff may also
os.system('rm /etc/apt/sources.list.d/*.bck')
# these are just to clear any other backed up sources
os.system('rm /etc/apt/sources.list.d/*.bak')
os.system('rm /etc/apt/sources.list.d/*.backup')
# add ppas for cool software
printGreen('Checking for and adding PPA\'s...')
if os.path.exists('/usr/sbin/apt-fast') != True:
	# add apt fast from ppa, this will speed up the install process a lot
	printGreen('Installing apt-fast to speed up install process...')
	printGreen('Adding apt-fast PPA...')
	os.system('add-apt-repository ppa:apt-fast/stable')
	if os.path.exists('/usr/sbin/apt-fast') != True:
		# if apt-fast repos are not up to date then install
		# the local backup debs, apt-fast is really important
		# for the performance of this installer
		os.system('gdebi unsupportedPackages/apt-fast_32bit.deb')
		os.system('gdebi unsupportedPackages/apt-fast_64bit.deb')
if configData['soundAndVideoTools'] == 'y':
	if os.path.exists('/usr/bin/simplescreenrecorder') != True:
		#install a ppa for simple screen recorder
		print 'Adding PPA for Simple Screen Recorder...'
		os.system('add-apt-repository ppa:maarten-baert/simplescreenrecorder')
if configData['netflix'] == 'y':
	if os.path.exists('/usr/bin/netflix-desktop') != True:
		#install a ppa for netflix-desktop
		print 'Adding PPA for Netflix Desktop...'
		os.system('apt-add-repository ppa:ehoover/compholio')
if configData['basicSoftwareAndSecurity'] == 'y':
	if os.path.exists('/usr/share/xfce4/panel/plugins/whiskermenu.desktop') != True:
		#install a ppa for whisker menu
		print 'Adding PPA for Whisker Menu...'
		os.system('add-apt-repository ppa:gottcode/gcppa')
if configData['gamesAndEmulation'] == 'y' :
	if os.path.exists('/usr/bin/retroarch') != True:
		printGreen('Adding Retroarch PPA...');
		os.system('apt-add-repository ppa:hunter-kaller/ppa');
	if configData['steamGames'] == 'y' and os.path.exists('/usr/bin/steam') != True:
		# downloads and installs steam from the offical website, cant include locally since its not gpl
		try: # since the download may fail
			writeFile('unsupportedPackages/steam.deb',downloadFile('http://media.steampowered.com/client/installer/steam.deb'))
			os.system('gdebi unsupportedPackages/steam.deb --non-interactive')
		except:
			print (redtext+boldtext+'Steam Client Failed To Install Properly!'+resetTextStyle)
######################
# then update, this will add everything to the repo so you can install it
######################
print 'Updating Package Repos to add PPA\'s...'
os.system('apt-get update >> Install_Log.txt')
######################
# then do the install
######################
# install apt-fast first since all installs after depend on it
if os.path.exists('/usr/sbin/apt-fast') != True:
	# dont dump to the install log because it asks for configuration info in install
	printGreen('Installing apt-fast(wrapper for apt-get to dramatically improve speed)')
	os.system('apt-get install apt-fast --assume-yes')
if configData['gamesAndEmulation'] == 'y' :
	if os.path.exists('/usr/bin/playonlinux') != True:
		printGreen('Installing PlayOnLinx...');
		os.system('apt-fast install playonlinux --assume-yes');
if configData['soundAndVideoTools'] == 'y':
	if os.path.exists('/usr/bin/simplescreenrecorder') != True:
		#install a ppa for simple screen recorder
		printGreen('Installing Simple Screen Recorder(Screen Recording Software)...')
		os.system('apt-fast install simplescreenrecorder --assume-yes')
if configData['netflix'] == 'y':
	if os.path.exists('/usr/bin/netflix-desktop') != True:
		#install a ppa for netflix-desktop
		printGreen('Installing Netflix Desktop...')
		os.system('apt-fast install netflix-desktop --assume-yes')
if configData['basicSoftwareAndSecurity'] == 'y':
	if os.path.exists('/usr/bin/hackbox-darknet-setup') != True:
		#install software that sets up darknet access though privoxy  
		printGreen('Installing Darknet...')
		os.system('gdebi --non-interactive unsupportedPackages/hackbox-darknet')
		os.system('hackbox-darknet-setup')
########################################################################
if configData['updateCheck'] == 'y' :
	print 'Installing updates...';
	# May require user interaction so dont output into logfile
	os.system('update')
########################################################################
printBlue( '##################################################################')
printGreen('### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###')
printBlue( '##################################################################')
printGreen('### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###')
printBlue( '##################################################################')
printGreen('### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###')
printBlue( '##################################################################')
printGreen('### BEGINNING AUTOMATED SECTION OF INSTALL GO GRAB A COFFEE... ###')
printBlue( '##################################################################')
########################################################################
# Start main automated section
########################################################################
# Section Base System Setup
#~ if configData['baseSystemCheck'] == 'y' :
	#~ try:
		#~ # get the username of the person running the program
		#~ username = os.getlogin()
	#~ except:
		#~ # above will fail if in a non cli system
		#~ print 'Program is not being run from a CLI system!'
		#~ print 'For the base system to install you must install from a command'
		#~ print 'line system (such as a server edition), program will now close.'
		#~ exit()
	#~ # Copy over preconfigured settings
	#makeDir(('/home/'+username+'/.local'))
	#COPY('./preconfiguredSettings/.local/',('/home/'+username+'/.local/'))
	#makeDir(('/home/'+username+'/.qshutdown'))
	#COPY('./preconfiguredSettings/.qshutdown/',('/home/'+username+'/.qshutdown/'))
	#makeDir(('/home/'+username+'/.config'))
	#COPY('./preconfiguredSettings/.config/',('/home/'+username+'/.config/'))
	#~ # Install Desktop window manager
	#~ printGreen('Installing Xfce (desktop)...');
	#~ os.system('apt-get install xfce4 --assume-yes >> Install_Log.txt');
	#~ printGreen('Installing Policy Kit (Regular Desktop Privlages)...');
	#~ os.system('apt-get install policykit-desktop-privileges --assume-yes >> Install_Log.txt');
	#~ printGreen('Installing Audio Support...');
	#~ os.system('apt-get install pulseaudio --assume-yes >> Install_Log.txt');
	#~ ####################################################################
	#~ #setup user group premissions
	#~ # add the user to the video and audio group so framebuffer will work
	#~ os.system('adduser '+username+' video')
	#~ os.system('adduser '+username+' audio')
	#~ os.system('adduser '+username+' adm')
	#~ # below is for a temporary hack to fix a problem with thunar
	#~ # being unable to mount drives, internal or exteral
	#~ os.system('adduser '+username+' storage')
	#~ ####################################################################
	#~ # below is for a bug fix, for using slim display manager with thunar
	#~ # fix automatic mounting with thunar on system
	#~ # create a group for storage mounting privlages
	#~ os.system('addgroup storage') 
	#~ # write config file to fix error
	#~ programFile = open('/etc/polkit-1/localauthority/50-local.d/org.freedesktop.udisks.pkla','w')
	#~ temp = '[Local Users]\n'
	#~ temp += 'Identity=unix-group:storage\n'
	#~ temp += 'Action=org.freedesktop.udisks.*\n'
	#~ temp += 'ResultAny=yes\n'
	#~ temp += 'ResultInactive=no\n'
	#~ temp += 'ResultActive=yes'
	#~ programFile.write(temp)
	#~ programFile.close()
	#~ ####################################################################
#~ else:
	#~ print 'Skipping Section...';
# Section for basic software / security needs
#  basic and security tools are installed by default now
#  this must remain a variable for later refactoring of the code
configData['basicSoftwareAndSecurity'] = 'y'
if configData['basicSoftwareAndSecurity'] == 'y' :
	########################################################################
	try:# check if less than one gig of memory, if so install fluxbox
		memory  = loadFile('/proc/meminfo').split('\n')[0].split(':')[1]
		while memory.find(' '):
			memory = memory.replace(' ','')
		memory = int(memory.replace('kB',''))
		if memory < 1000000:# if system memory is less than one gig
			os.system('apt-fast install fluxbox --assume-yes >> Install_Log.txt')
			os.system('apt-fast install volumeicon-alsa --assume-yes >> Install_Log.txt')
			os.system('apt-fast install midori --assume-yes >> Install_Log.txt')
	except:
		print ('ERROR: Could not correctly check system memory!')
	# install window manager/desktop enviorments
	os.system('apt-fast install xfce4 --assume-yes >> Install_Log.txt')
	# below is linux mint version of xfce desktop
	if os.path.exists('/lib/plymouth/themes/mint-logo'):
		os.system('apt-fast install mint-meta-xfce --assume-yes >> Install_Log.txt')
	else:
		# below is ubuntu version of xfce desktop
		os.system('apt-fast install xubuntu-desktop --assume-yes >> Install_Log.txt')
	# install sources file
	installSourcesFile('sources/basicSoftware.sources')
	# Set custom grub splash screen
	# move the .jpg file from the local media folder to /boot/grub/
	shutil.copy(os.path.abspath(os.path.join(os.curdir,'media','splash.jpg')),os.path.join('/boot','grub','splash.jpg'))
	# edit the grub settings to make the timeout 2 seconds insted of 5 for faster boot
	replaceLineInFile('/etc/default/grub','GRUB_TIMEOUT="','GRUB_TIMEOUT="2"')
	# run sudo update-grub to make grub regonize the new splash image
	os.system('sudo update-grub')
	####################################################################
	# adds 'system-info' command to the computer that simply invokes
	# 'inxi -F'. This will display system information in a nice clean 
	# way when you need to know something.
	printGreen('Installing inxi (System Info Display)..');
	os.system('apt-fast install inxi --assume-yes >> Install_Log.txt');
	# make linking script
	print 'Creating symbolic command system-info to axcess inxi...'
	programFile = open('/usr/bin/system-info','w')
	temp = '#! /bin/bash\n'
	temp += 'inxi -F'
	programFile.write(temp)
	programFile.close()
	os.system('chmod +x /usr/bin/system-info')
	####################################################################
	# install the clear history command on the system and set it to run
	# on every user logout to clear up space
	#~ os.system('python '+os.path.join(currentDirectory(),'clearHistory','setup.py'))
	# the replacing system for clearhistory uses the .bash_logout scripts. although
	# they do not work on lightdm, only under mdm
	# In the current mdm implementation these dont work on logout so
	# the below fixes that in the config of mdm
	if os.path.exists('/etc/mdm/PostSession/Default'):
		replaceLineInFileOnce('/etc/mdm/PostSession/Default','exit 0','bash $HOME/.bash_logout\nexit 0')
	# change the working directory back to the one holding this file
	#~ os.chdir(currentDirectory())#this is kinda unnessary since it no longer runs the install that way
	####################################################################
	# Setup programs to autostart when the user logs into the system
	# copy the .desktop files for programs into /etc/xdg/autostart
	# .desktop files are stored in /usr/share/applications
	COPY('/usr/share/applications/synapse.desktop','/etc/xdg/autostart')
	####################################################################
	# Install Icon Themes, and libnotify themes
	try:
		print 'Installing Faenza Icon Pack...'
		zipfile.ZipFile(os.path.join(currentDirectory(),'media/icons/Faenza.zip')).extractall('/usr/share/icons')
	except:
		print 'ERROR: Failed to install : Faenza Icons'
	try:
		print 'Installing Nitrux Icon Pack...'
		zipfile.ZipFile(os.path.join(currentDirectory(),'media/icons/Nitrux.zip')).extractall('/usr/share/icons')
	except:
		print 'ERROR: Failed to install : Nitrux Icons'
	try:
		print 'Installing Libnotify Theme...'
		zipfile.ZipFile(os.path.join(currentDirectory(),'media/themes/Smoke.zip')).extractall('/usr/share/themes')
	except:
		print 'ERROR: Failed to install : Libnotify Theme'
	# install Font Themes
	makeDir('/usr/share/fonts/truetype/hackbox')# make a custom font directory
	COPY(os.path.join(currentDirectory(),'media/fonts/'),'/usr/share/fonts/truetype/hackbox')
	# refresh the font cache to activate new font
	os.system('fc-cache -f -v')
	# Install logos and media
	makeDir('/usr/share/pixmaps/hackbox')
	makeDir('/usr/share/pixmaps/wallpapers')
	os.system('cp -rv media/wallpapers/. /usr/share/pixmaps/wallpapers/')
	COPY(os.path.join(currentDirectory(),'media/hackboxLogo.png'),'/usr/share/pixmaps/hackbox')
	COPY(os.path.join(currentDirectory(),'media/hackboxLogoText.png'),'/usr/share/pixmaps/hackbox')
	
	####################################################################
	# Make system links to fix some hardcoded call errors in programs
	# create a system link that sends calls for nautilus/nemo to thunar
	if os.path.exists('/usr/bin/cinnamon') != True:
		# use a if statement since cinnamon crashes without nemo
		os.system('sudo apt-fast purge nemo --assume-yes')
		os.system('link /usr/bin/thunar /usr/bin/nemo')
	# fuck nautilus and gnome 3
	os.system('sudo apt-fast purge nautilus --assume-yes')
	os.system('link /usr/bin/thunar /usr/bin/nautilus')
		
	################################################################
	# Setting Up Network Security
	####################################################################
	# install gui for managing the firewall and configure it to be turned on at boot 
	printGreen('Installing Gufw Firewall GUI...');
	os.system('apt-fast install gufw --assume-yes >> Install_Log.txt');
	print 'Configuring firewall to launch at boot...';
	os.system('ufw enable');
	####################################################################
	# unlock firewall ports for lan share on right click
	####################################################################
	prefix = '.'.join(socket.gethostbyname(socket.gethostname()+'.local').split('.')[:3])
	os.system('sudo ufw allow from '+prefix+'.0/24 to any port 9119')
	####################################################################
	# copy over the preconfigured settings for new users, extract from correct zipfile
	print 'Running editing default user settings in /etc/skel...'
	if configData['bottomBar'] == 'y':# want a desktop with the bar on the bottom
		zipfile.ZipFile('preconfiguredSettings/preconfiguredSettings_Bottom.zip','r').extractall('/etc/skel')
	else:# otherwise place that bar on top
		zipfile.ZipFile('preconfiguredSettings/preconfiguredSettings.zip','r').extractall('/etc/skel')
	# os.system('cp -vrf preconfiguredSettings/. /etc/skel') # this is now done though zipfiles above
	#~ print 'Editing specific aplications for current user...'
	#~ os.system('resetsettings -p goldendict')
	#~ os.system('resetsettings -p qshutdown')
	#~ os.system('resetsettings -p xarchiver')
	#~ os.system('resetsettings -p synapse')
	#~ os.system('resetsettings -p guake')
	#~ os.system('resetsettings -p radiotray')
	####################################################################
	# set zsh to the default shell for new users
	os.system('useradd -D -s $(which zsh)')
	# set zsh to default shell for current users
	os.system('sed -i.bak "s/bash/zsh/g" /etc/passwd')
	# remove backup file created by sed above
	os.system('rm -fv /etc/passwd.bak')
	####################################################################
	# install preload if pc has more than 4 gigs of ram, this will attempt
	# to preload libs the user usses often to ram reducing startup time of
	# commonly used programs
	try:
		memory  = loadFile('/proc/meminfo').split('\n')[0].split(':')[1]
		while memory.find(' '):
			memory = memory.replace(' ','')
		memory = int(memory.replace('kB',''))
		if memory > 4000000:# if memory is greater than 4 gigs
			os.system('apt-fast install preload --assume-yes >> Install_Log.txt')
	except:
		print ('ERROR: Could not install preload!')
	####################################################################
else:
	print 'Skipping Section...';

print '##################################################################'
print '  __  ___    _   __'
print ' /_ |/ _ \  (_) / /'
print '  | | | | |    / / '
print '  | | | | |   / /  '
print '  | | |_| |  / / _ '
print '  |_|\___/  /_/ (_)'
print '##################################################################'
# system tools
if configData['systemTools'] == 'y' :
	installSourcesFile('sources/systemTools.source')
else:
	print 'Skipping Section...';

print '##################################################################'
print '  ___   ___    _   __'
print ' |__ \ / _ \  (_) / /'
print '    ) | | | |    / / '
print '   / /| | | |   / /  '
print '  / /_| |_| |  / / _ '
print ' |____|\___/  /_/ (_)'
print '##################################################################'
# Section for office software
if configData['officeSoftware'] == 'y' :
	installSourcesFile('sources/officeSoftware.source')
else:
	print 'Skipping Section...';

print '##################################################################'
print '  ____   ___    _   __'
print ' |___ \ / _ \  (_) / /'
print '   __) | | | |    / / '
print '  |__ <| | | |   / /  '
print '  ___) | |_| |  / / _ '
print ' |____/ \___/  /_/ (_)'
print '##################################################################'
# Section for graphics tools
if configData['graphicsTools'] == 'y' :
	installSourcesFile('sources/graphicsTools.source')
else:
	print 'Skipping Section...';

print '##################################################################'
print '  _  _    ___    _   __'
print ' | || |  / _ \  (_) / /'
print ' | || |_| | | |    / / '
print ' |__   _| | | |   / /  '
print '    | | | |_| |  / / _ '
print '    |_|  \___/  /_/ (_)'
print '##################################################################'
# sound and video
if configData['soundAndVideoTools'] == 'y' :
	installSourcesFile('sources/soundAndVideoSoftware.source')
else:
	print 'Skipping Section...';

print '##################################################################'
print '  _____  ___    _   __'
print ' | ____|/ _ \  (_) / /'
print ' | |__ | | | |    / / '
print ' |___ \| | | |   / /  '
print '  ___) | |_| |  / / _ '
print ' |____/ \___/  /_/ (_)'
print '##################################################################'
# web design tools
if configData['webDesignTools'] == 'y' :
	installSourcesFile('sources/webDesignTools.source')
else:
	print 'Skipping Section...';

print '##################################################################'
print '    __   ___    _   __'
print '   / /  / _ \  (_) / /'
print '  / /_ | | | |    / / '
print ' |  _ \| | | |   / /  '
print ' | (_) | |_| |  / / _ '
print '  \___/ \___/  /_/ (_)'
print '##################################################################'
# section for programming tools
if configData['programmingTools'] == 'y' :
	installSourcesFile('sources/programmingTools.source')
	try:
		print 'Installing custom launchers...'
		zipfile.ZipFile(os.path.join(currentDirectory(),'preconfiguredSettings/launchers/programmingTools.zip')).extractall('/usr/share/applications')
	except:
		print 'ERROR: Failed to install : Launchers for programming section!'
else:
	print 'Skipping Section...';

print '##################################################################'
print '  ______ ___    _   __'
print ' |____  / _ \  (_) / /'
print '     / / | | |    / / '
print '    / /| | | |   / /  '
print '   / / | |_| |  / / _ '
print '  /_/   \___/  /_/ (_)'
print '##################################################################'
# Games & Emulation / Other Shit
if configData['gamesAndEmulation'] == 'y' :
	# NOTE playonlinux requires user interaction and is installed first
	installSourcesFile('sources/gamesAndEmulation.source')
	####################################################################
	# install useability command for listing all bsd games
	printGreen('Installing Bsd Games (usability commands)...');
	programFile = open('/usr/bin/bsdgames','w')
	temp = '#! /bin/bash\n'
	temp += 'echo "Use the below commands to access the individual games"\n'
	temp += 'echo "-----------------------------------------------------"\n'
	temp += 'echo "ninvaders - a ascii clone of Invaders"\n'
	temp += 'echo "adventure - an exploration game"\n'
	temp += 'echo "arithmetic - quiz on simple arithmetic"\n'
	temp += 'echo "atc - air traffic controller game"\n'
	temp += 'echo "backgammon - the game of backgammon"\n'
	temp += 'echo "banner - print large banner on printer"\n'
	temp += 'echo "battlestar - a tropical adventure game"\n'
	temp += 'echo "bcd - reformat input as punch cards, paper tape or morse code"\n'
	temp += 'echo "boggle - word search game"\n'
	temp += 'echo "caesar - decrypt caesar cyphers"\n'
	temp += 'echo "canfield - the solitaire card game canfield"\n'
	temp += 'echo "cfscores - show scores for canfield"\n'
	temp += 'echo "cribbage - the card game cribbage"\n'
	temp += 'echo "fish - play Go Fish"\n'
	temp += 'echo "gomoku - game of 5 in a row"\n'
	temp += 'echo "hangman - Computer version of the game hangman"\n'
	temp += 'echo "hunt - a multi-player multi-terminal game"\n'
	temp += 'echo "huntd - hunt daemon, back-end for hunt game"\n'
	temp += 'echo "mille - play Mille Bornes"\n'
	temp += 'echo "monop - Monopoly game"\n'
	temp += 'echo "morse - reformat input as punch cards, paper tape or morse code"\n'
	temp += 'echo "number - convert Arabic numerals to English"\n'
	temp += 'echo "phantasia - an interterminal fantasy game"\n'
	temp += 'echo "pom - display the phase of the moon"\n'
	temp += 'echo "ppt - reformat input as punch cards, paper tape or morse code"\n'
	temp += 'echo "primes - generate primes"\n'
	temp += 'echo "quiz - random knowledge tests"\n'
	temp += 'echo "rain - animated raindrops display"\n'
	temp += 'echo "random - random lines from a file or random numbers"\n'
	temp += 'echo "robots - fight off villainous robots"\n'
	temp += 'echo "rot13 - rot13 encrypt/decrypt"\n'
	temp += 'echo "sail - multi-user wooden ships and iron men"\n'
	temp += 'echo "snake - display chase game"\n'
	temp += 'echo "teachgammon - learn to play backgammon"\n'
	temp += 'echo "tetris-bsd - the game of tetris"\n'
	temp += 'echo "trek - trekkie game"\n'
	temp += 'echo "wargames - shall we play a game?"\n'
	temp += 'echo "worm - Play the growing worm game"\n'
	temp += 'echo "worms - animate worms on a display terminal"\n'
	temp += 'echo "wtf - translates acronyms for you"\n'
	temp += 'echo "wump - hunt the wumpus in an underground cave "\n'
	programFile.write(temp)
	programFile.close()
	os.system('sudo chmod +x /usr/bin/bsdgames')
	# install secondary command to list bsdgames using a system link
	os.system('link /usr/bin/bsdgames /usr/bin/bsd-games')
	
else:
	print 'Skipping Section...';

print '##################################################################'
print '   ___   ___    _   __'
print '  / _ \ / _ \  (_) / /'
print ' | (_) | | | |    / / '
print '  > _ <| | | |   / /  '
print ' | (_) | |_| |  / / _ '
print '  \___/ \___/  /_/ (_)'
print '##################################################################'
# Installs webcam support with cheese
if configData['webcamCheck'] == 'y' :
	# Installs cheese webcam software
	printGreen('Installing cheese (Webcam photobooth)...');
	os.system('apt-fast install cheese --assume-yes >> Install_Log.txt');
else:
	print 'Skipping section...';
# Installs flash and all of ubuntus restricted codecs and DVD support
if configData['restrictedExtras'] == 'y' :
	# Installs flash and all of ubuntus restricted codecs
	printGreen('Installing Restricted Extras...');
	os.system('apt-fast install ubuntu-restricted-extras --assume-yes >> Install_Log.txt');
	# the folloing commands install libdvdcss which allows dvd playback on ubuntu
	printGreen('Installing codecs to watch dvds...');
	os.system('apt-fast install libdvdread4 --assume-yes >> Install_Log.txt');
	os.system('/usr/share/doc/libdvdread4/install-css.sh')
else:
	print 'Skipping section...';

print '##################################################################'
print '   ___   ___    _   __'
print '  / _ \ / _ \  (_) / /'
print ' | (_) | | | |    / / '
print '  \__, | | | |   / /  '
print '    / /| |_| |  / / _ '
print '   /_/  \___/  /_/ (_)'
print '##################################################################'
########################################################################
# section for applying custom desktop config files
########################################################################
if configData['customSettingsCheck'] == 'y':
	if configData['basicSoftwareAndSecurity'] == 'y': # if basic section runs this is in there and dont need to run again
		print 'Running editing default user settings in /etc/skel...'
		if configData['bottomBar'] == 'y':# want a desktop with the bar on the bottom
			zipfile.ZipFile('preconfiguredSettings/preconfiguredSettings_Bottom.zip','r').extractall('/etc/skel')
		else:# otherwise place that bar on top
			zipfile.ZipFile('preconfiguredSettings/preconfiguredSettings.zip','r').extractall('/etc/skel')
		os.system('chown -R root /etc/skel')
	# run reset settings for all users on the system to apply custom desktop
	temp = os.listdir('/home')
	for user in temp:
		if user != 'lost+found' and user[:1] != '.':
			os.system('resetsettings -u '+user)
	#~ #remove distro info files
	#~ deleteFile(os.path.join('/etc','os-release'))
	#~ deleteFile(os.path.join('/etc','lsb-release'))
	#~ # replace distro info files, with premade ones
	#~ COPY(os.path.join('media','releaseFiles','os-release'),os.path.join('/etc','os-release'))
	#~ COPY(os.path.join('media','releaseFiles','lsb-release'),os.path.join('/etc','lsb-release'))
	# copy the mdm theme over 
	#~ try:
########################################################################
# install custom fonts for all users on system
########################################################################
os.system('cp -v media/fonts/* /usr/share/fonts/truetype/')
os.system('fc-cache -f -v')
#########################################################################
# Customize login to ttys and fix issues with bootlogo
########################################################################
# fix mintsystem reseting the below variables by turning off that crap
os.system('sed -i.bak "s/lsb-release = True/lsb-release = False/g" /etc/linuxmint/mintSystem.conf')
os.system('sed -i.bak "s/etc-issue = True/etc-issue = False/g" /etc/linuxmint/mintSystem.conf')
# customize the login of tty terminals
os.system('cp -vf media/ttyTheme/issue /etc/issue')
os.system('cp -vf media/ttyTheme/issue.net /etc/issue.net')
# add message of the day
os.system('sed -i.bak "s/exit 0//g" /etc/rc.local')
os.system('sed -i.bak "s/fortune > \/etc\/motd\.tail//g" /etc/rc.local')
os.system('echo "fortune > /etc/motd.tail" >> /etc/rc.local')
os.system('echo "exit 0" >> /etc/rc.local')
# copy over motd scripts
os.system('cp -rvf media/ttyTheme/update-motd.d/ /etc/')
# fix permissions on motd scripts
os.system('chmod +x /etc/update-motd.d/*')
os.system('chmod o-r /etc/update-motd.d/*')
os.system('chmod ug+r /etc/update-motd.d/*')
os.system('chmod u+w /etc/update-motd.d/*')
########################################################################
# apply branding to boot sequence for linux mint
# this will always be done regardless of user settings
########################################################################
if os.path.exists('/lib/plymouth/themes/mint-logo/'): #edit linux mint boot themes
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/mint-logo/bootlogo.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/mint-logo/logo.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/mint-logo/shutlogo.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/mint-logo/text.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/no-logo/no_logo.png')
if os.path.exists('/lib/plymouth/themes/xubuntu-logo/'):# edit xubuntu boot themes
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/xubuntu-logo/logo.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/xubuntu-logo/logo_16bit.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/xubuntu-logo/text.png')
if os.path.exists('/lib/plymouth/themes/ubuntu/'): # edit ubuntu boot themes
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/ubuntu/logo.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/ubuntu/logo_16bit.png')
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/themes/ubuntu/text.png')
if os.path.exists('/lib/plymouth/ubuntu_logo.png'):# edit main ubuntu boot logos
	os.system('cp -v media/hackboxLogoText.png /lib/plymouth/ubuntu_logo.png')
# rebuild config for plymouth
os.system('update-initramfs -u')
########################################################################
# Edit the login managers
########################################################################
print 'Installing Hackbox MDM Theme...'
# pull unzip theme into theme folder
if os.path.exists('/etc/mdm/mdm.conf'):
	zipfile.ZipFile(os.path.join('media','mdmTheme','HackBoxMdmTheme.zip'),'r').extractall('/usr/share/mdm/themes')
	# edit the default config to set the mdm theme
	replaceLineInFile('/etc/mdm/mdm.conf','Greeter=','\n\n')
	replaceLineInFile('/etc/mdm/mdm.conf','[security]','\nGreeter=/usr/lib/mdm/mdmgreeter\n\n[security]\n')
	replaceLineInFile('/etc/mdm/mdm.conf','GraphicalTheme=','\n\n')
	replaceLineInFile('/etc/mdm/mdm.conf','[greeter]','\n[greeter]\nGraphicalTheme=HackBox\n')
	replaceLineInFile('/etc/mdm/mdm.conf','DefaultSession=','DefaultSession=xfce.desktop')
	temp = loadFile('/etc/mdm/mdm.conf')
	# make shure nothing is more than double returned
	while (temp.find('\n\n\n') != -1):
		temp = temp.replace('\n\n\n','\n\n')
	writeFile('/etc/mdm/mdm.conf',temp)
	temp = None
if os.path.exists('/etc/lightdm/lightdm.conf'): # edit lightdm theme
	# disable guest session
	#~ os.chdir('/usr/lib/lightdm')
	#~ os.system('./lightdm-set-defaults --allow-guest=false')
	#~ os.chdir(currentDirectory())# reset back to current directory
	# edit the default settings
	replaceLineInFile('/etc/lightdm/lightdm.conf','greeter-session=','greeter-session=lightdm-gtk-greeter')
	replaceLineInFile('/etc/lightdm/lightdm.conf','user-session=','user-session=xubuntu')
	replaceLineInFile('/etc/lightdm/lightdm.conf','allow-guest=','allow-guest=false')
if os.path.exists('/etc/lightdm/unity-greeter.conf'):
	# edit the theme
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','logo=','logo=/usr/share/pixmaps/hackbox/media/hackboxLogo.png')
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','font-name=','font-name=Hermit 11')
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','icon-theme-name=','icon-theme-name=NITRUX')
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','user-session=','user-session=xfce')
	replaceLineInFile('/etc/lightdm/unity-greeter.conf','theme-name=','theme-name=Greybird')
if os.path.exists('/etc/lightdm/lightdm-gtk-greeter.conf'):
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','logo=','logo=/usr/share/pixmaps/hackbox/media/hackboxLogo.png')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','font-name=','font-name=Hermit 11')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','icon-theme-name=','icon-theme-name=NITRUX')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','user-session=','user-session=xfce')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','theme-name=','theme-name=Greybird')
if os.path.exists('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf'):
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','logo=','logo=/usr/share/pixmaps/hackbox/hackboxLogo.png')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','font-name=','font-name=Hermit 11')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','icon-theme-name=','icon-theme-name=NITRUX')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','user-session=','user-session=xfce')
	replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','theme-name=','theme-name=Greybird')
########################################################################
# Start automated install of special checklist items
########################################################################
if configData['redShiftCheck'] == 'y':
	printGreen('Installing Redshift...')
	os.system('sudo apt-fast install gtk-redshift --assume-yes >> Install_Log.txt')
	COPY('preconfiguredSettings/launchers/unsorted/redshift.desktop','/etc/xdg/autostart/')
else:
	print 'Skipping Redshift Install...';
########################################################################
# autoremove packages that are no longer needed & delete downloaded packages
print 'Cleaning up...'
os.system('apt-fast autoremove --assume-yes >> Install_Log.txt')
os.system('apt-fast clean >> Install_Log.txt')
clear();
print '##################################################################'
print '  __  ___   ___    _   __'
print ' /_ |/ _ \ / _ \  (_) / /'
print '  | | | | | | | |    / / '
print '  | | | | | | | |   / /  '
print '  | | |_| | |_| |  / / _ '
print '  |_|\___/ \___/  /_/ (_)'
print '##################################################################'
print 'Script finished system setup complete :D';
print defaultText
if os.path.exists('/etc/mdm/Init/Default'):
	# clear the mdm configured startup of hackboxsetup
	os.system('sed -i.bak "s/hackboxsetup\-gui\ \-\-no\-reset//g" /etc/mdm/Init/Default')
	os.system('sed -i.bak "/^$/d" /etc/mdm/Init/Default')# clear blank lines
	os.system('rm -fv /etc/mdm/Init/Default.bak')# remove backups from sed
if ('--no-reset' in sys.argv) != True:
	# check to see if the user set it to logout to set the settings
	if configData['customSettingsCheckLogout'] == 'y':
		os.system('killall Xorg')
# reboot check
if configData['rebootCheck'] == 'y' and configData['customSettingsCheckLogout'] != 'y':
	countdown = 10
	while countdown > 0:
		print 'System will REBOOT in',countdown,'seconds!'
		print 'Press Ctrl-C to Cancel Reboot!'
		countdown -= 1;
	print 'Rebooting the system NOW...'
	os.system('reboot')
# exit the script
raw_input('Press enter to end the script...')
exit(); 
