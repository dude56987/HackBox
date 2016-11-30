#! /usr/bin/python3
########################################################################
# Program Designed to setup a new Linux system automatically via scripts
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
import os, sys
from time import sleep
from random import randrange
########################################################################
sys.path.append('/opt/hackbox/')
import hackboxlib
import hackboxgui
########################################################################
Version = '0.5.0'
# For Ubuntu Server Edition/Ubuntu Desktop Edition/Linux Mint
########################################################################
#TODO:
# ~ custom distro???
########################################################################
# if the user is running the help command
if ("--help" in sys.argv) or ("-h" in sys.argv):
	print("########################################################################")
	print("# Program Designed to setup a new Linux system automatically via scripts")
	print("#  Copyright (C) 2015  Carl J Smith")
	print("#")
	print("#  This program is free software: you can redistribute it and/or modify")
	print("#  it under the terms of the GNU General Public License as published by")
	print("#  the Free Software Foundation, either version 3 of the License, or")
	print("#  (at your option) any later version.")
	print("#")
	print("#  This program is distributed in the hope that it will be useful,")
	print("#  but WITHOUT ANY WARRANTY; without even the implied warranty of")
	print("#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
	print("#  GNU General Public License for more details.")
	print("#")
	print("#  You should have received a copy of the GNU General Public License")
	print("#  along with this program.  If not, see <http://www.gnu.org/licenses/>.")
	print("########################################################################")
	print("--help or -h")
	print("\tDisplay this message.")
	print("--create-relay")
	print("\tSets up a torrent relay server.")
	print("\tUse the connect-to-relay command to connect to relay servers.")
	print("--force-use-config")
	print("\tDo not ask the user questions and just install the currently built")
	print("\tpayload.")
	print("--no-curses")
	print("\tDon't use the curses dialogs.")
	print("--force-reboot")
	print("\tReboot the system after the install process is finished.")
	print("--force-logout")
	print("\tForce the system to logout of whatever session is active for the")
	print("\tcurrent user.")
	print("--upgrade or -u")
	print("\tUpgrade this software with the latest version from git, then run it.")
	print("--changes or -c")
	print('\tShow the changes since last run with "--upgrade".')
	print("--changelog or -C")
	print("\tShow the entire changelog since the project was moved into version control.")
	print("########################################################################")
	# end the program after displaying the help menu
	exit()
########################################################################
# Pre-run checks
print('Preforming startup checks...')
# run program as root if it is not being already done
if os.geteuid() != 0:
	# try to run the program with dialog
	os.system('sudo python3 '+(os.path.abspath(__file__))+' '+(' '.join(sys.argv[1:])))
	exit()
########################################################################
if ("--create-relay" in sys.argv):
	# run the setup-relay-server script to set the current copy in /opt/hackbox/update to act as a master relay
	os.system('bash /opt/hackbox/scripts/relayScripts/server-setup-relay.sh')
	exit()
########################################################################
if ("--upgrade" in sys.argv) or ("-u" in sys.argv) or ("--update" in sys.argv):
	# upgrade hackbox with the latest version from git or the latest version from your setup relay server
	if os.path.exists("/etc/hackbox/relayServer"):
		# copy over the pull relay script to run as a cron job
		os.system('cp -f /opt/hackbox/scripts/relayScripts/client-pull-from-relay.sh /etc/cron.daily/00-hackbox-client-pull-relay')
		os.system('chmod +x /etc/cron.daily/00-hackbox-client-pull-relay')
		# launch the previously created update script if it has not been launched already
		os.system("bash /etc/cron.daily/00-hackbox-client-pull-relay")
	else:
		# if the system has not updated before pull a update
		if not os.path.exists('/opt/hackbox/update/'):
			# run clone and if it fails run a pull to update
			os.system('git clone https://github.com/dude56987/HackBox.git /opt/hackbox/update/ || git -C /opt/hackbox/update/ pull')
		# store the existing updates
		os.system('git -C /opt/hackbox/update/ log > /etc/hackbox/changes.old')
		# pull the latest version from git
		os.system('git clone https://github.com/dude56987/HackBox.git /opt/hackbox/update/ || git -C /opt/hackbox/update/ pull')
		os.system('git -C /opt/hackbox/update/ log > /etc/hackbox/changes.new')
		# check for system changes without overwriting the changes log
		changes = os.system('diff /etc/hackbox/changes.old /etc/hackbox/changes.new')
		# if no changes were found no updates need to be done
		if changes == 0:
			print('No updates found, exiting HackBox Setup!')
		else:
			# changes were found, so write the new update changes to the log
			os.system('diff /etc/hackbox/changes.old /etc/hackbox/changes.new > /etc/hackbox/changes.log')
			# the system needs to build and install the updates
			os.system('cd /opt/hackbox/update/;make install')
			os.system('hackboxsetup --force-use-config')
	exit()
########################################################################
if ("--changes" in sys.argv) or ("-c" in sys.argv):
	if os.path.exists('/etc/hackbox/changes.log'):
		# show changes in last update and exit
		os.system('less /etc/hackbox/changes.log')
		exit()
	else:
		anwser = hackboxgui.askQuestion('No updates have been done to detect changes! Would you like to update HackBox?')
		if anwser == 'y':
			os.system('hackboxsetup --update')
			os.system('hackboxsetup --changes')
			exit()
		else:
			print('Nothing has been done, exiting HackBox Setup!')
			exit()
########################################################################
if ("--changelog" in sys.argv) or ("-C" in sys.argv):
	if os.path.exists('/etc/hackbox/changes.new'):
		os.system('git -C /opt/hackbox/update/ log')
		exit()
	else:
		anwser = hackboxgui.askQuestion('No updates have been done to detect changes! Would you like to update HackBox?')
		if anwser == 'y':
			os.system('hackboxsetup --update')
			os.system('hackboxsetup --changelog')
			exit()
		else:
			print('Nothing has been done, exiting HackBox Setup!')
			exit()
########################################################################
# set current directory to be same as this file
os.chdir('/opt/hackbox')
# create the install log
os.system('echo "Starting Install Process..." > Install_Log.txt');
os.system('echo "Started on ${date}" >> Install_Log.txt');
# only prompt the user if --force-use-config is not used in the program launch
if (('--force-use-config' in sys.argv) == False):
	if (("--no-curses" in sys.argv) != True):
		question = 'This script will install and configure settings for a new system automatically.\n\n'
		question += 'Proceed?'
		# returns 0 for yes and 1 for no
		if hackboxgui.askQuestion(question) == 'y':
			print('Starting setup...')
		else:
			hackboxlib.clear();
			print('Ending script...')
			exit();
	else:
		if os.path.exists('/opt/hackbox/media/banner.txt'):
			print(hackboxlib.loadFile('/opt/hackbox/media/banner.txt'))
		# prompt user if they want to proceed or not
		hackboxlib.colorText('<bluetext>This script will install and configure settings for a new \n system automatically.</>')
		check = input('Proceed? [y/n]: ')
		if check == 'y' :
			print('Starting setup...')
		else:
			hackboxlib.clear();
			print('Ending script...')
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
	print('Checking Network Connection...')
	# pick a random website from the list above
	website =  websites[(randrange(0,(len(websites)-1)))]
	connected = bool(hackboxlib.downloadFile(website))
	if connected == False:
		print('Connection failed, please connect to the network!')
		for i in range(20):
			print('Will retry again in '+str(20-int(i))+' seconds...')
			sleep(1)
########################################################################
hackboxlib.clear()
os.chdir('/opt/hackbox')
# create the install payload file, it will be installed after this stuff
payloadFileLocation = hackboxlib.createInstallLoad(sys.argv)
########################################################################
# run some commands that will keeps the screen from blanking during install
# these will fail in the terminal but that wont stop the program
os.system('xset s 0 0')
os.system('xset s off')
os.system('xset -dpms')
########################################################################
# install the payload created previously
hackboxlib.installSourcesFile(payloadFileLocation)
# show 100 percent at end
hackboxgui.progressBar(100,'Script finished, System setup complete :D',"Hackbox Setup")
os.system('nohup broadcast 100% System setup complete :D> /dev/null')
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
		print('System will REBOOT in '+countdown+' seconds!')
		print('Press Ctrl-C to Cancel Reboot!')
		countdown -= 1;
	print('Rebooting the system NOW...')
	os.system('reboot')
# exit the script
