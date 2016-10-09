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
import os, sys
from time import sleep
from random import randrange
sys.path.append('/opt/hackbox/')
import hackboxlib
########################################################################
Version = '0.5.0'
# For Ubuntu Server Edition/Ubuntu Desktop Edition/Linux Mint
########################################################################
#TODO:
# ~ custom distro???
########################################################################
# use the gui if it exists
if (("--no-curses" in sys.argv) != True):
	#from dialog import Dialog
	import dialog
	queryboxes = dialog.Dialog()
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
	print("########################################################################")
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
print('Preforming startup checks...')
# run program as root if it is not being already done
if os.geteuid() != 0:
	if len(sys.argv) > 1:
		os.system('sudo python3 '+(os.path.abspath(__file__))+' '+sys.argv[1])
	else:
		os.system('sudo python3 '+(os.path.abspath(__file__)))
	exit()
# set current directory to be same as this file
os.chdir('/opt/hackbox')
# create the install log
os.system('echo "Starting Install Process..." >> Install_Log.txt');
os.system('echo "Started on ${date}" >> Install_Log.txt');
# set the background for the dialouges
if (("--no-curses" in sys.argv) != True):
	queryboxes.setBackgroundTitle("HackBox Setup")
# only prompt the user if --force-use-config is not used in the program launch
if (('--force-use-config' in sys.argv) == False):
	if (("--no-curses" in sys.argv) != True):
		temp = 'This script will install and configure settings for a new system automatically.\n\n'
		temp += 'Proceed?'
		# returns 0 for yes and 1 for no
		if (queryboxes.yesno(temp)=='ok'):
			print('Starting setup...')
		else:
			hackboxlib.clear();
			print('Ending script...')
			exit();
	else:
		# prompt user if they want to proceed or not
		hackboxlib.colorText('<bluetext>This script will install and configure settings for a new \n system automatically.</>')
		check = raw_input('Proceed? [y/n]: ')
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
payloadFileLocation = hackboxlib.createInstallLoad()
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
hackboxlib.progressBar(100,'Script finished, System setup complete :D',"Hackbox Setup")
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
