#! /bin/bash
########################################################################
# Script to setup custom login themes
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
# Graphical Login Manager
########################################################################
# install the lightdm gtk login manager
apt-get install lightdm --assume-yes
apt-get install lightdm-gtk-greeter --assume-yes
# install the gui to edit the login settings
apt-get install lightdm-gtk-greeter-settings --assume-yes
# copy over the login theme for the lightdm gtk greeter
cp -fv /opt/hackbox/media/loginThemes/lightdmGtkTheme/lightdm-gtk-greeter.conf /etc/lightdm/lightdm-gtk-greeter.conf
# Set the lightdm-gtk-greeter to be the default lightdm greeter
echo '[SeatDefaults]' > /usr/share/lightdm/lightdm.conf.d/90-hackbox.conf
echo 'greeter-session=lightdm-gtk-greeter'>> /usr/share/lightdm/lightdm.conf.d/90-hackbox.conf
echo 'user-session=xfce'>> /usr/share/lightdm/lightdm.conf.d/90-hackbox.conf
echo 'allow-guest=false'>> /usr/share/lightdm/lightdm.conf.d/90-hackbox.conf
echo 'greeter-hide-users=false'>> /usr/share/lightdm/lightdm.conf.d/90-hackbox.conf
########################################################################
# TTY Login Manager
########################################################################
# Customize login to ttys and fix issues with bootlogo
# customize the login of tty terminals
cp -vf /opt/hackbox/media/ttyTheme/issue /etc/issue
cp -vf /opt/hackbox/media/ttyTheme/issue.net /etc/issue.net
# fix mintsystem reseting the above variables by turning off that crap
sed -i "s/lsb-release = True/lsb-release = False/g" /etc/linuxmint/mintSystem.conf
sed -i "s/etc-issue = True/etc-issue = False/g" /etc/linuxmint/mintSystem.conf
