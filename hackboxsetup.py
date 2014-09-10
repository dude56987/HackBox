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
import os, sys, shutil, json, zipfile, socket, urllib2, md5
from time import sleep
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
resetTextStyle=defaultText
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
		#print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		#sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	#print "Finished Loading :",fileName
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
			#print 'Wrote file:',fileName
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
		return False
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
def colorText(text):
	defaultText='\033[0m'
	text= text.replace('<defaultText>',defaultText)
	boldtext='\033[1m'
	text= text.replace('<boldtext>',boldtext)
	blinktext='\033[5m'
	text= text.replace('<blinktext>',blinktext)
	#textcolors
	blacktext = '\033[30m'
	text= text.replace('<blacktext>',blacktext)
	redtext= '\033[31m'
	text= text.replace('<redtext>',redtext)
	greentext= '\033[32m'
	text= text.replace('<greentext>',greentext)
	yellowtext= '\033[33m'
	text= text.replace('<yellowtext>',yellowtext)
	bluetext= '\033[34m'
	text= text.replace('<bluetext>',bluetext)
	magentatext= '\033[35m'
	text= text.replace('<magentatext>',magentatext)
	cyantext= '\033[36m'
	text= text.replace('<cyantext>',cyantext)
	whitetext= '\033[37m'
	text= text.replace('<whitetext>',whitetext)
	#background colors
	blackbackground= '\033[40m'
	text= text.replace('<blackbackground>',blackbackground)
	redbackground= '\033[41m'
	text= text.replace('<redbackground>',redbackground)
	greenbackground= '\033[42m'
	text= text.replace('<greenbackground>',greenbackground)
	yellowbackground= '\033[43m'
	text= text.replace('<yellowbackground>',yellowbackground)
	bluebackground= '\033[44m'
	text= text.replace('<bluebackground>',bluebackground)
	magentabackground= '\033[45m'
	text= text.replace('<magentabackground>',magentabackground)
	cyanbackground= '\033[46m'
	text= text.replace('<cyanbackground>',cyanbackground)
	whitebackground= '\033[47m'
	text= text.replace('<whitebackground>',whitebackground)
	# reset to default style
	resetTextStyle=defaultText+blackbackground+whitetext
	text= text.replace('</>',resetTextStyle)
	return text
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
	# setup progress calculations
	progressPercent = ''
	progress = 0.0
	progressTotal = len(fileObject)
	# go though each line of the file
	for line in fileObject:
		# calc progress and display
		writeFile('/tmp/INSTALLPROGRESS.txt',('%'+str((progress/progressTotal)*100)+' completed...'))
		progress += 1
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
				if tempInfo[1]=='CHECK-PACKAGE-MANAGER':
					# reset the package manager, perfer apt-fast
					packageManager=False
					if os.path.exists('/usr/bin/apt-get'):
						packageManager = 'apt-get'
					if os.path.exists('/usr/sbin/apt-fast'):
						packageManager = 'apt-fast'
					if packageManager == False:
						return False
				if tempInfo[1] == 'message':
					printGreen(tempInfo[2]+'...')
				elif tempInfo[1] == 'script':
					os.system('bash scripts/'+tempInfo[2]+'.sh')
				elif tempInfo[1] == 'command':
					# execute command
					print tempInfo[2]
					os.system(tempInfo[2])
				elif tempInfo[1] == 'deb-repo':
					# add a debian repo and keyfile for that repo
					#######################
					# create a filename from the url given for the repo
					fileName=(tempInfo[2].replace('.','_').replace('/','').replace(' ','_').replace(':',''))+'.list'
					# if repo does not already exist
					if os.path.exists(('/etc/apt/sources.list.d/'+fileName)) != True:
						# if a deb repo to add, add the repo as its own file in sources.list.d
						writeFile(('/etc/apt/sources.list.d/'+fileName),tempInfo[2])
						# then add the key to the repo
						downloadedKeyFile=downloadFile(tempInfo[3])
						keyFileName=(tempInfo[3].replace('.','_').replace('/','').replace(' ','_').replace(':',''))+'.pgp'
						if downloadedKeyFile != False:
							writeFile(('/tmp/'+keyFileName),downloadedKeyFile)
							os.system('apt-key add /tmp/'+keyFileName)
							os.system('rm /tmp/'+keyFileName)
							#os.system(('apt-get update -o Dir::Etc::sourcelist="sources.list.d/'+fileName+'" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"'))
						else:
							# if the key is not downloaded delete the repo
							os.system('rm /etc/apt/sources.list.d/'+fileName)
				elif tempInfo[1] == 'ppa':
					# if the package is a ppa source to add, use --yes to suppress confirmation
					os.system(('apt-add-repository '+tempInfo[2]+' --yes'))
					## BELOW IS BROKEN AS FUCK, above is a hackaround ##
					# update only the added repo using its location in /etc/apt/sources.list.d/
					# user must currently define this in the last argument in a ppa command
					#os.system(('apt-get update -o Dir::Etc::sourcelist="sources.list.d/'+tempInfo[3]+'" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"'))
				elif tempInfo[1] == 'rm-package':
					#/usr/share/doc/packagename is checked to see if the package has already been installed
					# remove package
					if (os.path.exists('/usr/share/doc/'+tempInfo[2])):
						os.system((packageManager+' purge '+tempInfo[2]+' --assume-yes >> Install_Log.txt'))
				elif tempInfo[1] == 'package':
					#/usr/share/doc/packagename is checked to see if the package has already been installed
					# install package
					if (os.path.exists('/usr/share/doc/'+tempInfo[2]) != True):
						os.system((packageManager+' install '+tempInfo[2]+' --assume-yes >> Install_Log.txt'))
				elif tempInfo[1] == 'localdeb':
					# install package in unsupported packages
					tempInfo[2] = 'unsupportedPackages/'+tempInfo[2]+'.deb'
					if os.path.exists(tempInfo[2]): 
						# create a md5 from the file
						tempMD5 = md5.new(loadFile(tempInfo[2])).digest()
						print (tempMD5)
						if os.path.exists(tempInfo[2]+".md5"):
							if loadFile(tempInfo[2]+".md5") == tempMD5:
								print "No new file, package not installed."
							else:
								# if no parity is found write a new md5 and install the new file	
								writeFile((tempInfo[2]+'.md5'),tempMD5)
								os.system(('sudo gdebi --no '+tempInfo[2]))
						else:
							# if file does not have a md5 file yet create one and install the program
							writeFile((tempInfo[2]+'.md5'),tempMD5)
							os.system(('sudo gdebi --no '+tempInfo[2]))
					else:
						print ("ERROR:No "+tempInfo[2]+" exists!")
	return True
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
			useConfig = raw_input('[y/n]:')
			if useConfig == 'y':
				installSourcesFile('/etc/hackbox/payload.source')
				return True
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
		clear()
		# go though each line of the file
		for line in fileObject:
			# all lines starting with # are comments
			if line[:13]=='#AUTO-INSTALL':
				# skip the question
				installSection = 'y'
			elif line[:6]=='#INFO:':
				# print the info
				print line[6:]
			elif line[:7]=='#BANNER':
				# print the colorized banner file
				banner = loadFile('media/banner.txt')
				if banner != False:
					print (colorText(banner))
			elif line[:10]=='#QUESTION:':
				# check for install confrimation
				if installSection != 'y':# if the AUTO-INSTALL is not set
					print (line[10:])# show question
					installSection = raw_input('[y/n]:')# display prompt on a newline for y/n
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
os.chdir('/opt/hackbox')
# banner to show the program
clear()
print colorText(loadFile('media/banner.txt'))
print 'Designed for:'+greentext+'Ubuntu Desktop Edition/Linux Mint Xfce Edition'+resetTextStyle
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
# Check for network connection, dont proceed unless it is active
connected = False
from random import randrange
while connected == False:
	print 'Checking Network Connection...'
	websites = []
	websites.append('http://www.linuxmint.com')
	websites.append('http://www.distrowatch.com')
	websites.append('http://www.duckduckgo.com')
	websites.append('http://www.ubuntu.com')
	websites.append('http://www.wikipedia.org')
	# pick a random website from the list above
	website =  websites[(randrange(0,(len(websites)-1)))]
	connected = bool(downloadFile(website))
	if connected == False:
		print 'Connection failed, please connect to the network!'
		for i in range(20):
			print ('Will retry again in '+str(20-int(i))+' seconds...')
			sleep(1)
########################################################################
clear();
os.chdir(currentDirectory())
# create the install payload file, it will be installed after this stuff
payloadFileLocation = createInstallLoad()
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
# TODO: MAKE ALL THE BELOW STUFF INTO SCRIPTS AND SOURCE FILES          #
#########################################################################
#########################################################################
#########################################################################
#########################################################################
#########################################################################
# create the install log
os.system('echo "Starting Install Process..." >> Install_Log.txt');
os.system('echo "Started on ${date}" >> Install_Log.txt');
########################################################################
# run some commands that will keeps the screen from blanking during install
# these will fail in the terminal but that wont stop the program
os.system('xset s 0 0')
os.system('xset s off')
os.system('xset -dpms')
########################################################################
# cleanup sources, above leaves backup files, other stuff may also
os.system('rm /etc/apt/sources.list.d/*.bck')
# these are just to clear any other backed up sources
os.system('rm /etc/apt/sources.list.d/*.bak')
os.system('rm /etc/apt/sources.list.d/*.backup')
########################################################################
# install window manager/desktop enviorments
os.system('apt-fast install xfce4 --assume-yes >> Install_Log.txt')
# below is linux mint version of xfce desktop
#if os.path.exists('/lib/plymouth/themes/mint-logo'):
#	os.system('apt-fast install mint-meta-xfce --assume-yes >> Install_Log.txt')
#else:
	# below is ubuntu version of xfce desktop
#	os.system('apt-fast install xubuntu-desktop --assume-yes >> Install_Log.txt')
# install sources file
# Set custom grub splash screen
# move the .jpg file from the local media folder to /boot/grub/
shutil.copy(os.path.abspath(os.path.join(os.curdir,'media','splash.jpg')),os.path.join('/boot','grub','splash.jpg'))
# edit the grub settings to make the timeout 2 seconds insted of 5 for faster boot
replaceLineInFile('/etc/default/grub','GRUB_TIMEOUT="','GRUB_TIMEOUT="2"')
# run sudo update-grub to make grub regonize the new splash image
os.system('sudo update-grub')
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
# Install Icon Themes, and libnotify themes
iconPacks = os.listdir('/opt/hackbox/media/icons')
for pack in iconPacks:
	try:
		zipfile.ZipFile(os.path.join(currentDirectory(),('/opt/hackbox/media/icons/'+pack))).extractall('/usr/share/icons')
	except:
		print 'ERROR: Failed to install icon pack at',('/opt/hackbox/media/icons/'+pack)
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
try:
	prefix = '.'.join(socket.gethostbyname(socket.gethostname()+'.local').split('.')[:3])
	os.system('sudo ufw allow from '+prefix+'.0/24 to any port 9119')
except:
	print ("Failed to dertermine lan structure!")
	print ("Share on lan will fail!")
####################################################################
# set zsh to the default shell for new users
os.system('useradd -D -s $(which zsh)')
# set zsh to default shell for current users
os.system('sed -i "s/bash/zsh/g" /etc/passwd')
####################################################################
# install preload if pc has more than 4 gigs of ram, this will attempt
# to preload libs the user usses often to ram reducing startup time of
# commonly used programs
try:
	memory  = loadFile('/proc/meminfo').split('\n')[0].split(':')[1]
	while memory.find(' '):
		memory = memory.replace(' ','')
	memory = int(memory.replace('kB',''))
	if memory > 1600000:# if memory is greater than 4 gigs
		os.system('apt-fast install preload --assume-yes >> Install_Log.txt')
except:
	print ('ERROR: Could not install preload!')
####################################################################
# Games & Emulation 
# NOTE playonlinux requires user interaction and is installed first
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
########################################################################
# install custom fonts for all users on system
########################################################################
os.system('cp -v media/fonts/* /usr/share/fonts/truetype/')
os.system('fc-cache -f -v')
#########################################################################
# Customize login to ttys and fix issues with bootlogo
########################################################################
# fix mintsystem reseting the below variables by turning off that crap
os.system('sed -i "s/lsb-release = True/lsb-release = False/g" /etc/linuxmint/mintSystem.conf')
os.system('sed -i "s/etc-issue = True/etc-issue = False/g" /etc/linuxmint/mintSystem.conf')
# customize the login of tty terminals
os.system('cp -vf media/ttyTheme/issue /etc/issue')
os.system('cp -vf media/ttyTheme/issue.net /etc/issue.net')
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
# modify slim theme backgrounds
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
# install the payload created previously
installSourcesFile(payloadFileLocation)
print '##################################################################'
print '  __  ___   ___    _   __'
print ' /_ |/ _ \ / _ \  (_) / /'
print '  | | | | | | | |    / / '
print '  | | | | | | | |   / /  '
print '  | | |_| | |_| |  / / _ '
print '  |_|\___/ \___/  /_/ (_)'
print '##################################################################'
print 'Script finished system setup complete :D';
if os.path.exists('/etc/mdm/Init/Default'):
	# clear the mdm configured startup of hackboxsetup
	os.system('sed -i.bak "s/hackboxsetup\-gui\ \-\-no\-reset//g" /etc/mdm/Init/Default')
	os.system('sed -i.bak "/^$/d" /etc/mdm/Init/Default')# clear blank lines
	os.system('rm -fv /etc/mdm/Init/Default.bak')# remove backups from sed
# check to see if the user set it to logout to set the settings
if '--force-logout' in sys.argv:
	os.system('killall lxsession')
	os.system('killall xfce4-session')
# reboot check
if '--force-reboot' in sys.argv:
	countdown = 10
	while countdown > 0:
		print 'System will REBOOT in',countdown,'seconds!'
		print 'Press Ctrl-C to Cancel Reboot!'
		countdown -= 1;
	print 'Rebooting the system NOW...'
	os.system('reboot')
# exit the script
