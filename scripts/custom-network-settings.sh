#! /bin/bash
########################################################################
# Tweak network settings to fix problems in Ubuntu
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
echo "Checking network configuration..."
if grep '^hosts:' /etc/nsswitch.conf;then
	# This will fix mdns and hostname only resolution
	echo "Changing name resolution checking order..."
	sed -i -e "s/^hosts.*$/hosts:          files mdns4_minimal [NOTFOUND=return] dns resolve [!UNAVAIL=return] myhostname/g" /etc/nsswitch.conf
fi
# remove blank lines
echo "Removing blank lines..."
sed -i '/^$/d' /etc/nsswitch.conf
echo "Restarting networking..."
service networking restart
echo "Network tweaks done..."
