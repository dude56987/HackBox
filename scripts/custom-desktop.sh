#! /bin/bash
##############################################
# A script to setup login for a low ram system
##############################################
# set a global to use for absolute values
scriptPath="";
# check if the questions should be asked to the user
if [ -f /etc/hackbox/customDesktopSkipQuestions ];then
	#nuttin to do
	echo 'Skipping the questions...';
else
	# install top or bottom settings for panels
	if dialog --yesno "Would you like the bar on the bottom of the desktop(e.g. like windows)?:" 8 70;then
		echo '' > /etc/hackbox/customDesktopBottomBarYes;
		rm /etc/hackbox/customDesktopBottomBarNo;
	else
		echo '' > /etc/hackbox/customDesktopBottomBarNo;
		rm /etc/hackbox/customDesktopBottomBarYes;
	fi
	# the check on reseting existing users settings to defaults
	# check if the user would like to install the new settings for all current users
	if dialog --yesno "
Would you like to install the preset desktop settings over the current ones?\n\n
WARNING: This is only recommended if you are installing on a new system or
if you want all applications reset to the factory default state.\n\n
TLDR: y to delete your current settings, n to keep them.\n\n
Would you like to install the preset desktop settings?\n\n" 20 70;then
		echo '' > /etc/hackbox/customDesktopYes;
		rm /etc/hackbox/customDesktopNo;
	else
		echo '' > /etc/hackbox/customDesktopNo;
		rm /etc/hackbox/customDesktopYes;
	fi
	if dialog --yesno "Would you like to save your previous anwsers?" 20 70;then
		echo '' > /etc/hackbox/customDesktopSkipQuestions;
	else
		rm /etc/hackbox/customDesktopSkipQuestions;
	fi
fi
# reset the terminal to clean up after the dialog boxes
reset;
# nuke current /etc/skel to replace it with next stuff
rm -rvf /etc/skel/.*;
# install preconfigured settings for default of new users, CORE others below
unzip -o /opt/hackbox/preconfiguredSettings/userSettings/CORE.zip -d /etc/skel;
if [ -f /etc/hackbox/customDesktopBottomBarYes ];then
	unzip -o /opt/hackbox/preconfiguredSettings/userSettings/bottomBar.zip -d /etc/skel;
else
	# if not on the bottom the bar is placed on the top
	unzip -o /opt/hackbox/preconfiguredSettings/userSettings/topBar.zip -d /etc/skel;
fi
if [ -f /etc/hackbox/customDesktopYes ];then
	for dir in /home/*;do
		userName=$(echo "$dir" | sed "s/\/home\///g");
		resetsettings -u $userName;
	done
fi
exit 0
