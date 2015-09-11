#! /usr/bin/python3
########################################################################
# Program Designed to setup a new Linux system automatically via scripts
# Copyright (C) 2015  Carl J Smith
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
import os, sys, shutil, json, zipfile, socket, hashlib
from urllib.request import urlopen
from time import sleep
from random import randrange
########################################################################
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
# use the gui if it exists
if (("--no-curses" in sys.argv) != True):
	#from dialog import Dialog
	import dialog
	queryboxes = dialog.Dialog()
# define functions
########################################################################
def progressBar(percentage,messageText,banner):
	if (("--no-curses" in sys.argv) != True):
		percentage=int(percentage)
		messageText=str(messageText)
		progressBar = dialog.Dialog()
		progressBar.setBackgroundTitle(banner)
		progressBar.gauge_start(percent=percentage,text=messageText)#DEBUG
		#progressBar.gauge_update(percentage,messageText)#DEBUG
		progressBar.gauge_stop()#DEBUG
		return True
	else:
		percentage=str(percentage)
		messageText=str(messageText)
		print('#'*80)
		print(messageText)
		print(percentage+'%')
		print('#'*80)
########################################################################
def deleteFile(filePath):
	if os.path.exists(filePath):
		os.remove(filePath)
		return True
	else:
		print("ERROR: file does not exist, so can not remove it.")
		return False
########################################################################
def loadFile(fileName):
	try:
		#print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print("Failed to load : "+fileName)
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
			print('Failed to write file:'+fileName)
			return False
	else:
		print('Failed to write file, path:'+filepath+'does not exist!')
		return False
########################################################################
def downloadFile(fileAddress):
	#convert address to text string
	fileAddress=str(fileAddress)
	print("Downloading :"+fileAddress)
	try:
		downloadedFileObject = urlopen(fileAddress)
	except:
		print("Failed to download :"+fileAddress)
		return False
	# convert to text string
	downloadedFileObject = downloadedFileObject.readall()
	fileText = downloadedFileObject 
	print("Finished Loading :"+fileAddress)
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
					print('Replacing line:'+line)
					print('With:'+replacementText)
					newFileText += replacementText+'\n'
				else:
					print('Deleting line:'+line)
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
	''' Creates the defined directory, if a list of directories are listed
	that do not exist then they will be created as well, so beware of 
	spelling mistakes as this will create the specified directory you 
	type mindlessly.'''
	temp = remoteDir.split('/')
	remoteDir= ''
	for i in temp:
		remoteDir += (i + '/')
		if os.path.exists(remoteDir):
			print(remoteDir+' : Already exists!, Moving on...')
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
	print(temp)
########################################################################
def printGreen(text):
	temp = greentext+boldtext+text+resetTextStyle
	print(temp)
########################################################################
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
					print('ERROR: '+dest+' Already Exists, Will not Overwrite!')
					return False
				else:
					shutil.copytree(src,dest)
					return True
			else:
				#if src path does not exist throw a error and do not overwrite
				print('ERROR:'+src+'Does Not Exist!')
				return False
		except:
			print('ERROR: a unknown error occurred when copying'+src+'to'+dest)
			return False
########################################################################
def installSourcesFile(fileNameOfFile):
	'''Reads a source file of programs to install and installs them.'''
	# change this so that source files are split into 3 pieces of data
	# first the type of data, second the message to print, third the data
	# itself, the data would depend on the data type described in the first
	# space of the line
	if fileNameOfFile == False:
		# if the build process fails
		print("ERROR: payload.source failed to build!")
		return False
	packageManager=False
	if os.path.exists('/usr/bin/apt-get'):
		packageManager = 'apt-get'
	if os.path.exists('/usr/sbin/apt-fast'):
		packageManager = 'apt-fast'
	if packageManager == False:
		return False
	fileObject = loadFile(fileNameOfFile)
	if fileObject == False:
		print('ERROR: Source file'+fileNameOfFile+'does not exist!')
		return False
	else:
		fileObject = fileObject.split('\n')
	# setup progress calculations
	progressPercent = ''
	progress = 0.0
	progressTotal = len(fileObject)
	currentMessage = 'Starting install process...'
	# go though each line of the file
	for line in fileObject:
		readSourcesFileLine(line)	
		# this is at bottom of loop outside of if tree	
		if showUpdate == True:
			# calc progress and display
			if (("--no-curses" in sys.argv) != True):
				progressBar(int((progress/progressTotal)*100),currentMessage,'Hackbox Setup')
			else:
				writeFile('/tmp/INSTALLPROGRESS.txt',('%'+str((progress/progressTotal)*100)+' completed...'))
		progress += 1
	return True
########################################################################
def readSourceFileLine(line):
	''' Reads a single line from a source file. Then takes aproprate 
	action based on what the configuration option is. For more info
	on configuration options you can read the INFO file in the 
	/opt/hackbox/sources/ directory.'''
	# set a variable to show update progress
	showUpdate=True
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
				if (("--no-curses" in sys.argv) != True):
					currentMessage=(tempInfo[2]+'...')
				else:
					printGreen(tempInfo[2]+'...')
			elif tempInfo[1] == 'script':
				# dont update progress bar 
				# the scripts pump out a bunch of text
				showUpdate=False
				if os.path.exists('/opt/hackbox/scripts/'+tempInfo[2]+'.sh'):
					# launch the script in bash if its a shell script
					os.system('bash /opt/hackbox/scripts/'+tempInfo[2]+'.sh')
				elif os.path.exists('/opt/hackbox/scripts/'+tempInfo[2]+'.py'):
					# launch program in python if its a python script
					os.system('python3 /opt/hackbox/scripts/'+tempInfo[2]+'.py')
			elif tempInfo[1] == 'command':
				# execute command
				if (("--no-curses" in sys.argv) != True):
					currentMessage=tempInfo[2]
				else:
					print(tempInfo[2])
				# print the command to the install log
				os.system('echo "'+tempInfo[2]+'" >> Install_Log.txt')
				os.system(tempInfo[2]+' >> Install_Log.txt')
			elif tempInfo[1] == 'deb-repo':
				# dont update progress bar this part pumps out a bunch of text
				showUpdate=False
				# add a debian repo and keyfile for that repo
				#######################
				# create a clean filename from the url given for the repo
				fileName=(tempInfo[2].strip())
				fileName=(fileName.replace('.','_'))
				fileName=(fileName.replace('/',''))
				fileName=(fileName.replace(' ','_'))
				fileName=(fileName.replace(':',''))
				fileName=(fileName.replace('https',''))
				fileName=(fileName.replace('http',''))
				fileName=(fileName.replace('deb_',''))
				fileName=(fileName.replace('__','_'))
				fileName=(fileName.replace('___','_'))
				# remove _ at the start of filename
				fileName=(fileName.replace('^_',''))
				# The repo info will be overwritten if it already exists
				# if a deb repo to add, add the repo as its own file in sources.list.d
				writeFile(('/etc/apt/sources.list.d/'+fileName+'.list'),tempInfo[2])
				# then add the key to the repo
				downloadedKeyFile=downloadFile(tempInfo[3])
				if downloadedKeyFile != False:
					''' This section contains some commented out code. The reason for this
					Is that I think there is a better way to add keyfiles by directly
					writing them into the keyfile directly. You may have to write them as
					binary files. This is untested though and the current implementation
					works now. In the future I would like to do this without apt-key but
					right now it still works with apt-key '''
					# write file to temp and add keyfile with apt-key
					writeFile(('/tmp/'+str(fileName)+'.gpg'),downloadedKeyFile.decode('utf8'))
					os.system('apt-key add /tmp/'+str(fileName)+'.gpg')
					# clear the key from temp
					os.system('rm /tmp/'+str(fileName)+'.gpg')
					# write keyfile directly to trusted keyfile directory
					#writeFile(('/etc/apt/trusted.gpg.d/'+str(fileName)+'.gpg'),downloadedKeyFile.decode('utf8'))
					# update this newly added repo
					#os.system(('apt-get update -o Dir::Etc::sourcelist="sources.list.d/'+fileName+'" -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"'))
				else:
					# if the key is not downloaded delete the repo
					os.system('rm /etc/apt/sources.list.d/'+str(fileName)+'.list')
			elif tempInfo[1] == 'open-port':
				# allow traffic from inside the given port
				os.system('sudo ufw allow proto tcp from any to any port '+tempInfo[2])
			elif tempInfo[1] == 'open-lan-port':
				try:
					# dertermine the lan prefix we are on
					prefix = '.'.join(socket.gethostbyname(socket.gethostname()+'.local').split('.')[:3])
					# allow traffic from inside the given port
					os.system('sudo ufw allow proto tcp from '+prefix+'.0/24 to any port '+tempInfo[2])
				except:
					print("ERROR: Failed to dertermine lan structure!")
					print("ERROR: Cannot open port "+tempInfo[2]+" on lan!")
			elif tempInfo[1] == 'ppa':
				# dont update progress bar this part pumps out a bunch of text
				showUpdate=False
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
				tempInfo[2] = '/opt/hackbox/unsupportedPackages/'+tempInfo[2]+'.deb'
				if os.path.exists(tempInfo[2]): 
					hashObject=hashlib.md5()
					#fileObject=open(tempInfo[2],'rb')
					with open(tempInfo[2], "rb") as fileObject:
						temp = fileObject.read(128)
						hashObject.update(temp)
					# load the file to be converted to md5
					#tempMD5 = loadFile(tempInfo[2])
					#tempMD5 = str(tempMD5)
					# encode file content string into bytes
					#tempMD5 = tempMD5.encode('utf-8')
					#tempMD5 = tempMD5.encode('utf-8')
					# feed the bytes into a md5 hash object
					#tempMD5 = hashlib.md5(tempMD5)
					# convert the hash into a readable string
					tempMD5 = hashObject.hexdigest()
					#print (tempMD5)
					if os.path.exists(tempInfo[2]+".md5"):
						if loadFile(tempInfo[2]+".md5") == tempMD5:
							pass
							#print "No new file, package not installed."
						else:
							# if no parity is found write a new md5 and install the new file	
							writeFile((tempInfo[2]+'.md5'),tempMD5)
							os.system(('sudo gdebi --no '+tempInfo[2]))
					else:
						# if file does not have a md5 file yet create one and install the program
						writeFile((tempInfo[2]+'.md5'),tempMD5)
						os.system(('sudo gdebi --no '+tempInfo[2])+' >> Install_Log.txt')
				else:
					print("ERROR:No "+tempInfo[2]+" exists!")
########################################################################
def createInstallLoad():
	useConfig = 'n'
	# check if a payload has already been built
	if os.path.exists('/etc/hackbox/sources/configured'):
		if ('--force-use-config' in sys.argv):
			# create a config file based on the setup options
			useConfig = 'y'
		else:
			if (("--no-curses" in sys.argv) != True):
				# returns 0 for yes and 1 for no
				if queryboxes.yesno('A config already exists, would you like to use it?')=='ok':
					useConfig = 'y'
				else:
					useConfig = 'n'
					os.system('rm -rvf /etc/hackbox/*')
			else:
				# otherwise ask the user if they want to use it
				print('A config already exists, would you like to use it?')
				useConfig = raw_input('[y/n]:')
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
		# set the install section here to keep it in the scope of the file	
		installSection = 'n'
		# if the source file has already been configured use previous config
		if useConfig == 'y':
			# if use has set to use previous configuration and if file exists
			if os.path.exists(os.path.join('/etc/hackbox/sources/',fileName)):
				installSection = 'y'
			else:
				#if file does not exist do not install the section
				installSection = 'n'
		# open the .source file
		fileObject = loadFile(os.path.join('sources',fileName))
		if fileObject == False:
			print('ERROR: Source file'+fileName+'does not exist!')
		else:
			fileObject = fileObject.split('\n')
		# clear the screen before loading stuff in this file
		clear()
		# go though each line of the file
		backgroundTitle = ""
		for line in fileObject:
			# all lines starting with # are comments
			if line[:13]=='#AUTO-INSTALL':
				# skip the question
				installSection = 'y'
			elif line[:6]=='#INFO:':
				# print the info
				print(line[6:])
			elif line[:7]=='#BANNER':
				# print the colorized banner file
				banner = loadFile('media/banner.txt')
				if banner != False:
					if (("--no-curses" in sys.argv) != True):
						backgroundTitle = 'Hackbox Setup'
						if line[:8]=='#BANNER:':
							backgroundTitle =  line[8:]
					else:
						print(colorText(banner))
			elif line[:10]=='#QUESTION:':
				# check for install confrimation
				if installSection != 'y' and useConfig != 'y':# if the AUTO-INSTALL is not set
					if (("--no-curses" in sys.argv) != True):
						# returns 0 for yes and 1 for no
						if queryboxes.yesno(line[10:]) == 'ok':
							# write file for next run
							writeFile(os.path.join('/etc/hackbox/sources/',fileName),'')
							installSection = 'y'
						else:
							installSection = 'n'
					else:
						print(line[10:])# show question
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
		# extract any preconfigured launchers included for this section
		if os.path.exists(('/opt/hackbox/preconfiguredSettings/launchers/'+fileName.split('.')[0]+'.zip')):
			mainPayload += 'null<:>command<:>unzip -o '+'/opt/hackbox/preconfiguredSettings/launchers/'+fileName.split('.')[0]+'.zip -d /usr/share/applications\n'
	repoPayload += 'null<:>command<:>apt-get update\n'
	# orginize the payload contents
	payload = repoPayload+interactivePayload+prePayload+mainPayload+postPayload
	# write the payload to a text file
	writeFile('/etc/hackbox/payload.source',payload)
	# write configured file to show config has been built before on next run
	writeFile('/etc/hackbox/sources/configured','')
	# return the payload file location
	return '/etc/hackbox/payload.source'
########################################################################
