#! /bin/bash
##############################################
# A script to install the custom themes
##############################################
# This script installs the various custom themes
# and media assets included in HackBox for use in
# the system.
#########################################
# inctall custom icon themes in hackbox #
#########################################
for iconPack in /opt/hackbox/media/icons/*;do
	unzip -o /opt/hackbox/media/icons/$iconPack -d /usr/share/icons;
done
################################
# install the libnotify themes #
################################
for theme in /opt/hackbox/media/themes/libnotify/*;do
	unzip -o /opt/hackbox/media/themes/libnotify/$theme -d /usr/share/themes;
done
########################
# Install Custom Fonts #
########################
# create a directory to store customized fonts, this is for sanitys sake since all fonts in /usr/share/fonts/ are added by a recursive scan of the subdirectories 
mkdir -p /usr/share/fonts/hackbox/
# copy all fonts over to the hackbox fonts location
cp -vf /opt/hackbox/media/fonts/ /usr/share/fonts/hackbox/
# refresh the font index on the system to add new fonts
fc-cache -f -v
#############################
# Install custom wallpapers #
#############################
mkdir -p /usr/share/pixmaps/wallpapers
cp -vf /opt/hackbox/media/wallpapers/* /usr/share/pixmaps/wallpapers/
###############################
# Install logos to the system #
###############################
mkdir -p /usr/share/pixmaps/hackbox
cp -vf /opt/hackbox/media/*.jpg /usr/share/pixmaps/hackbox/
cp -vf /opt/hackbox/media/*.png /usr/share/pixmaps/hackbox/
# exit the script if everything worked out
exit 0
