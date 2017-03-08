#! /bin/bash
########################################################################
# Change the default firefox profile name to a hash of the profileName
# Copyright (C) 2017 Carl J Smith
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
# randomize the firefox profile name by basing it on the hostname as a hash
profileName=$(hostname | sha512sum | cut -d " " -f 1)
# use only the first 20 characters of the hash
profileName=${profileName:0:20}
# chanage default hackbox config into the new profile name
if [ -f /etc/skel/.mozilla/firefox/hackbox.default ];then
	# change the default profile to use the profileName
	mv /etc/skel/.mozilla/firefox/hackbox.default /etc/skel/.mozilla/firefox/$profileName.default
fi
if [ -f /etc/skel/.mozilla/firefox/profiles.ini ];then
	# change the default profile.ini file
	sed -i "s/hackbox/$profileName/g" /etc/skel/.mozilla/firefox/profiles.ini
fi
