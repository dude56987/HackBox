#! /bin/bash
########################################################################
# Change system affinity to use the swap partition
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
# change swap space setup
more /etc/sysctl.conf | grep swappiness 
if more /etc/sysctl.conf | grep swappiness ; then
	echo 'Nothing to be done...'
else
	echo 'Set swap to 15...'
	sudo bash -c "echo 'vm.swappiness = 15' >> /etc/sysctl.conf"	
fi
