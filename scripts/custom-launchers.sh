#! /bin/bash
########################################################################
# Script to install custom launchers
# Copyright (C) 2017  Carl J Smith
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
###################################
# Install the autostart launchers #
###################################
for launcher in /opt/hackbox/preconfiguredSettings/launchers/autostart/*;do
	if echo $launcher | grep "\.desktop";then
		# cleanup the filename so we can determine the new filename for permissions fixing
		fileName=$(echo "$launcher"| sed "s/\/opt\/hackbox\/preconfiguredSettings\/launchers\/autostart\///g")
		# copy over the launcher
		cp -v $launcher /etc/xdg/autostart/$fileName
		# set the permissions correctly on that launcher
		# permissions should be u = rw, g = r, o = r
		chmod -v u+rw,u-x,go-wx,go+r /etc/xdg/autostart/$fileName
	fi
done
##########################################
# Copy over custom application launchers #
##########################################
for launcher in /opt/hackbox/preconfiguredSettings/launchers/applications/*;do
	if echo $launcher | grep "\.desktop";then
		# cleanup the filename so we can determine the new filename for permissions fixing
		fileName=$(echo "$launcher"| sed "s/\/opt\/hackbox\/preconfiguredSettings\/launchers\/applications\///g")
		# copy over the launcher
		cp -v $launcher /usr/share/applications/$fileName
		# set the permissions correctly on that launcher
		# permissions should be u = rw, g = r, o = r
		chmod -v u+rw,u-x,go-wx,go+r /usr/share/applications/$fileName
	fi
done
# exit the script if everything worked out
exit 0
