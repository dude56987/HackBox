#! /bin/bash
########################################################################
# Script to setup custom login themes
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
# install the lightdm gtk login manager
apt-get install lightdm-gtk-greeter --assume-yes
# install the gui to edit the login settings
apt-get install lightdm-gtk-greeter-settings --assume-yes
# copy over the login theme
cp -fv /opt/hackbox/media/loginThemes/lightdmGtkTheme/lightdm-gtk-greeter.conf /etc/lightdm/lightdm-gtk-greeter.conf
