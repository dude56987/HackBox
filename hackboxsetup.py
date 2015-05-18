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
from random import randrange
sys.path.append('/opt/hackbox/')
import hackboxlib
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
# use the gui if it exists
if (("--no-curses" in sys.argv) != True):
	from dialog import Dialog
	queryboxes = Dialog()
########################################################################
# if the user is running the help command
if ("--help" in sys.argv) or ("-h" in sys.argv):
	print "########################################################################"
	print "# Program Designed to setup a new Linux system automatically via scripts"
	print "#  Copyright (C) 2015  Carl J Smith"
	print "#" 
	print "#  This program is free software: you can redistribute it and/or modify"
	print "#  it under the terms of the GNU General Public License as published by"
	print "#  the Free Software Foundation, either version 3 of the License, or"
	print "#  (at your option) any later version."
	print "#" 
	print "#  This program is distributed in the hope that it will be useful,"
	print "#  but WITHOUT ANY WARRANTY; without even the implied warranty of"
	print "#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
	print "#  GNU General Public License for more details."
	print "#" 
	print "#  You should have received a copy of the GNU General Public License"
	print "#  along with this program.  If not, see <http://www.gnu.org/licenses/>."
	print "########################################################################"
	print "--help or -h"
	print "\tDisplay this message."
	print "--create-relay"
	print "\tSets up a torrent relay server."
	print "\tUse the connect-to-relay command to connect to relay servers."
	print "--force-use-config"
	print "\tDo not ask the user questions and just install the currently built"
	print "\tpayload."
	print "--no-curses"
	print "\tDon't use the curses dialogs."
	print "--force-reboot"
	print "\tReboot the system after the install process is finished."
	print "--force-logout"
	print "\tForce the system to logout of whatever session is active for the"
	print "\tcurrent user."
	print "--upgrade or -u"
	print "\tUpgrade this software with the latest version from git, then run it."
	print "########################################################################"
	# end the program after displaying the help menu
	exit()
if ("--create-relay" in sys.argv):
	# run the setup-relay-server script to set the current copy in /opt/hackbox/update to act as a master relay
	os.system('sudo bash /opt/hackbox/scripts/relayScripts/server-setup-relay.sh')
	exit()
if ("--upgrade" in sys.argv) or ("-u" in sys.argv) or ("--update" in sys.argv):
	if os.path.exists("/etc/hackbox/relayServer"):
		# copy over the pull relay script to run as a cron job
		os.system('sudo cp -f /opt/hackbox/scripts/relayScripts/client-pull-from-relay.sh /etc/cron.daily/00-hackbox-client-pull-relay')
		os.system('sudo chmod +x /etc/cron.daily/00-hackbox-client-pull-relay')
		# launch the previously created update script if it has not been launched already
		os.system("sudo bash /etc/cron.daily/00-hackbox-client-pull-relay")
	else:
		# pull the latest version from git and install it
		os.system('sudo git clone https://github.com/dude56987/HackBox.git /opt/hackbox/update/ || sudo git -C /opt/hackbox/update/ pull')
		os.system('cd /opt/hackbox/update/;sudo make install')
		os.system('sudo hackboxsetup --force-use-config')
	exit()
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
hackboxlib.clear()
print hackboxlib.colorText(hackboxlib.loadFile('media/banner.txt'))
print 'Designed for:'+greentext+'Ubuntu Desktop Edition/Linux Mint Xfce Edition'+resetTextStyle
# set the background for the dialouges
if (("--no-curses" in sys.argv) != True):
	queryboxes.setBackgroundTitle("HackBox Setup")
# only prompt the user if --force-use-config is not used in the program launch
if (('--force-use-config' in sys.argv) == False):
	if (("--no-curses" in sys.argv) != True):
		temp = 'This script will install and configure settings for a new system automatically.\n\n'
		temp += 'Proceed?'
		# returns 0 for yes and 1 for no
		if queryboxes.yesno(temp)== 0:
			print 'Starting setup...';
		else:
			hackboxlib.clear();
			print 'Ending script...';
			exit();
	else:
		# prompt user if they want to proceed or not
		printBlue('This script will install and configure settings for a new \n system automatically.')
		check = raw_input('Proceed? [y/n]: ');
		if check == 'y' :
			print 'Starting setup...';
		else:
			hackboxlib.clear();
			print 'Ending script...';
			exit();
# Check for network connection, dont proceed unless it is active
connected = False
websites = []
websites.append('http://www.linuxmint.com')
websites.append('http://www.distrowatch.com')
websites.append('http://www.duckduckgo.com')
websites.append('http://www.ubuntu.com')
websites.append('http://www.wikipedia.org')
while connected == False:
	print 'Checking Network Connection...'
	# pick a random website from the list above
	website =  websites[(randrange(0,(len(websites)-1)))]
	connected = bool(hackboxlib.downloadFile(website))
	if connected == False:
		print 'Connection failed, please connect to the network!'
		for i in range(20):
			print ('Will retry again in '+str(20-int(i))+' seconds...')
			sleep(1)
########################################################################
hackboxlib.clear();
os.chdir('/opt/hackbox')
# create the install payload file, it will be installed after this stuff
payloadFileLocation = hackboxlib.createInstallLoad()
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
####################################################################
# install the clear history command on the system and set it to run
# on every user logout to clear up space
#~ os.system('python '+os.path.join(currentDirectory(),'clearHistory','setup.py'))
# the replacing system for clearhistory uses the .bash_logout scripts. although
# they do not work on lightdm, only under mdm
# In the current mdm implementation these dont work on logout so
# the below fixes that in the config of mdm
if os.path.exists('/etc/mdm/PostSession/Default'):
	hackboxlib.replaceLineInFileOnce('/etc/mdm/PostSession/Default','exit 0','bash $HOME/.bash_logout\nexit 0')
####################################################################
# Setting Up Network Security
####################################################################
# install gui for managing the firewall and configure it to be turned on at boot 
hackboxlib.printGreen('Installing Gufw Firewall GUI...');
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
# Games & Emulation 
# NOTE playonlinux requires user interaction and is installed first
####################################################################
# install useability command for listing all bsd games
hackboxlib.printGreen('Installing Bsd Games (usability commands)...');
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
	hackboxlib.replaceLineInFile('/etc/mdm/mdm.conf','Greeter=','\n\n')
	hackboxlib.replaceLineInFile('/etc/mdm/mdm.conf','[security]','\nGreeter=/usr/lib/mdm/mdmgreeter\n\n[security]\n')
	hackboxlib.replaceLineInFile('/etc/mdm/mdm.conf','GraphicalTheme=','\n\n')
	hackboxlib.replaceLineInFile('/etc/mdm/mdm.conf','[greeter]','\n[greeter]\nGraphicalTheme=HackBox\n')
	hackboxlib.replaceLineInFile('/etc/mdm/mdm.conf','DefaultSession=','DefaultSession=xfce.desktop')
	temp = hackboxlib.loadFile('/etc/mdm/mdm.conf')
	# make shure nothing is more than double returned
	while (temp.find('\n\n\n') != -1):
		temp = temp.replace('\n\n\n','\n\n')
	hackboxlib.writeFile('/etc/mdm/mdm.conf',temp)
	temp = None
if os.path.exists('/etc/lightdm/lightdm.conf'): # edit lightdm theme
	# disable guest session
	#~ os.chdir('/usr/lib/lightdm')
	#~ os.system('./lightdm-set-defaults --allow-guest=false')
	#~ os.chdir(currentDirectory())# reset back to current directory
	# edit the default settings
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm.conf','greeter-session=','greeter-session=lightdm-gtk-greeter')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm.conf','user-session=','user-session=xubuntu')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm.conf','allow-guest=','allow-guest=false')
if os.path.exists('/etc/lightdm/unity-greeter.conf'):
	# edit the theme
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','logo=','logo=/usr/share/pixmaps/hackbox/media/hackboxLogo.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','font-name=','font-name=Hermit 11')
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','icon-theme-name=','icon-theme-name=NITRUX')
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','user-session=','user-session=xfce')
	hackboxlib.replaceLineInFile('/etc/lightdm/unity-greeter.conf','theme-name=','theme-name=Greybird')
if os.path.exists('/etc/lightdm/lightdm-gtk-greeter.conf'):
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','logo=','logo=/usr/share/pixmaps/hackbox/media/hackboxLogo.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','font-name=','font-name=Hermit 11')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','icon-theme-name=','icon-theme-name=NITRUX')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','user-session=','user-session=xfce')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter.conf','theme-name=','theme-name=Greybird')
if os.path.exists('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf'):
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','background=','background=/usr/share/pixmaps/hackbox/wallpaperBranded.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','logo=','logo=/usr/share/pixmaps/hackbox/hackboxLogo.png')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','font-name=','font-name=Hermit 11')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','icon-theme-name=','icon-theme-name=NITRUX')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','user-session=','user-session=xfce')
	hackboxlib.replaceLineInFile('/etc/lightdm/lightdm-gtk-greeter-ubuntu.conf','theme-name=','theme-name=Greybird')
# install the payload created previously
hackboxlib.installSourcesFile(payloadFileLocation)
# show 100 percent at end
hackboxlib.progressBar(100,'Script finished, System setup complete :D',"Hackbox Setup")
if os.path.exists('/etc/mdm/Init/Default'):
	# clear the mdm configured startup of hackboxsetup
	os.system('sed -i "s/hackboxsetup\-gui\ \-\-no\-reset//g" /etc/mdm/Init/Default')
	os.system('sed -i "/^$/d" /etc/mdm/Init/Default')# clear blank lines
# copy over the default .xinitrc file
os.system('for dir in $(ls /home);do cp -f /etc/skel/.xinitrc /home/$dir/.xinitrc;chown $dir /home/$dir/.xinitrc;done')
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
