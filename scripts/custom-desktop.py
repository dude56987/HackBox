#! /usr/bin/python3
########################################################################
# Script to install custom desktop settings
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
import os
from dialog import Dialog
########################################################################
# TODO #################################################################
########################################################################
#     * Dialog with radio buttons to let the user pick the desktop they
#        want installed.
#     * Dialog to ask if the user wants to save those settings
#     * Dialog to ask if the user wants to overwrite the current settings
#        of all users on the system with the defaults
#     * Install CORE settings folder by default, ignore it in the dialogs
#     * Set a file to check for if the user wants the questions to be
#        skipped on update or new install
#       * Filename is flag, variables are read from the file itself
#     * Use resetsettings -u to reset all users on the system
########################################################################
# install the core settings by default
# check for config file that skips everything else
if os.path.exists('/etc/hackbox/customDesktop.conf'):
	deleteMe=False
	desktopLayout=False
	overwriteUsers=False
	# read the config file, order does not matter
	for line in open('/etc/hackbox/customDesktop.conf','r'):
		line=line.split('=')
		# remove line endings
		line[1]=line[1].replace('\n','')
		line[1]=line[1].replace('\r','')
		if line[0]=='overwriteUsers' and line[1]=='true':
			overwriteUsers=True
		elif line[0]=='desktopLayout':
			desktopLine=line[1]
		elif line[0]=='deleteMe' and line[1]=='true':
			deleteMe=True
	#######################################
	# begin applying config file set flags
	#######################################
	# clean up the old default configs
	os.system("rm -rvf /etc/skel/.*")
	os.system("rm -rvf /etc/skel/*")
	# install default core into /etc/skel 
	os.system("cp -rvf /opt/hackbox/preconfiguredSettings/userSettings/CORE/. /etc/skel")
	# install user picked settings package into the /etc/skel
	if len(desktopLine) > 1:
		print("cp -rvf "+desktopLine+"/. /etc/skel")
		os.system("cp -rvf "+desktopLine+"/. /etc/skel")
	if overwriteUsers==True:
		# overwrite the users default settings
		for user in os.listdir('/home/'):
			if (("." in user) or ("+" in user)) != True:
				print('resetsettings -u '+user)
				os.system('resetsettings -u '+user)
	if deleteMe==True:
		# remove the config file if usersettings are not saved
		os.system('rm /etc/hackbox/customDesktop.conf')
	# end the program to prevent a forever loop
	exit()
########################################################################
# create the root dialog object
root=Dialog()
choices=[]
config=''
########################################################################
# Build the user interface 
########################################################################
# grab a list of available default settings for the user to pick from
for item in os.listdir("/opt/hackbox/preconfiguredSettings/userSettings/"):
	if (item != "CORE") and (("." in item) != True):
		if "default" in item:
			choices.append((item,'',1))
		else:
			choices.append((item,'',0))
if len(choices)>1:
	userChoice=root.radiolist('Which desktop enviorment layout would you like to be the default?',20,60,15,choices)
	# returns a 2 value tuple, grab value # 1
	userChoice=("/opt/hackbox/preconfiguredSettings/userSettings/"+userChoice[1])
	# add to the config file
	config+=('desktopLayout='+userChoice+'\n')
########################################################################
# in the yesno dialog ok = yes, cancel = no 
if "ok" == root.yesno("Would you like to overwrite all users current settings with the new default settings?\n\nWARNING:This will delete any settings you have changed in your applications.However your documents will remain untouched.",20,60):
	config+='overwriteUsers=true\n'
else:
	config+='overwriteUsers=false\n'
########################################################################
if "ok" == root.yesno("Would you like to save these choices for next time you run the installer?",20,60):
	# set the flag to not delete the config file
	config+='deleteMe=false\n'
else:
	# set the flag to delete the config file
	config+='deleteMe=true\n'
########################################################################
# write the file
fileObject=open('/etc/hackbox/customDesktop.conf','w')
fileObject.write(config)
fileObject.close()
########################################################################
# Recursively call the script itself to read the configfile and apply
# the correct actions.
os.system('python3 /opt/hackbox/scripts/custom-desktop.py');
