#! /bin/bash
########################################################################
# Copy all systemd service files into the correct directory
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
# Copy over Hackbox systemd services directory onto system and enable them
########################################################################
cp -v /opt/hackbox/preconfiguredSettings/services/* /etc/systemd/system/
# enable and activate all new services
for service in /opt/hackbox/preconfiguredSettings/services/*;do
	# clean up path to get service name
	service=$(echo "$service" | sed "s/\.service//g")
	service=$(echo "$service" | sed "s/\/opt\/hackbox\/preconfiguredSettings\/services\///g")
	# enable the service so it will run at every boot
	systemctl enable $service
	# start the service
	systemctl start $service
done
