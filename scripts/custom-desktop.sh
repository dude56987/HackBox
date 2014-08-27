#! /bin/bash
##############################################
# A script to setup login for a low ram system
##############################################
# set a global to use for absolute values
scriptPath=""
# check if the user would like to install the new settings for all current users
echo "Would you like to install the preset desktop settings over the current ones?"
echo "WARNING: This is only recommended if you are installing on a new system or"
echo "         if you want all applications reset to the factory default state."
echo "TLDR: y to delete your current settings, n to keep them."
echo -n "Would you like to install the preset desktop settings? [y/n]:"
read resetUserSettings
# check if the user would like the bar on the bottom of the screen
echo -n "Would you like the bar on the bottom of the desktop(e.g. like windows)?[y/n]:"
read barOnBottom
# nuke current /etc/skel to replace it with next stuff
rm -rvf /etc/skel/.*
# install preconfigured settings for default of new users, CORE others below
unzip -o /opt/hackbox/preconfiguredSettings/userSettings/CORE.zip -d /etc/skel
# install top or bottom settings for panels
if [ "$barOnBottom" == "y" ]; then
	unzip -o /opt/hackbox/preconfiguredSettings/userSettings/bottomBar.zip -d /etc/skel
else
	# if not on the bottom the bar is placed on the top
	unzip -o /opt/hackbox/preconfiguredSettings/userSettings/topBar.zip -d /etc/skel
fi
# the check on reseting existing users settings to defaults
if [ "$resetUserSettings" == "y" ];then
	for dir in /home/*;do
		userName=$(echo "$dir" | sed "s/\/home\///g")
		resetsettings -u $userName
	done
fi
