#! /bin/bash
########################################################################
# Setup privoxy,tor,and i2p to work together to run for entire system
# Copyright (C) 2014  Carl J Smith
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
# install tor + privoxy
apt-get install tor --assume-yes
apt-get install privoxy --assume-yes
apt-get install macchanger --assume-yes
# setting up i2p deepweb protocall though ppa ##########################
if [ -f /usr/bin/i2prouter ];then
	# set anwsers for setup dialouges
	echo "i2p	i2p/daemon	boolean	true" > /tmp/i2p.conf
	echo "i2p	i2p/user	string	i2psvc" >> /tmp/i2p.conf
	echo "i2p	i2p/memory	string	128" >> /tmp/i2p.conf
	debconf-set-selections /tmp/i2p.conf
	# add ppa update and install program
	apt-add-repository ppa:i2p-maintainers/i2p --yes
	apt-get update
	apt-get install i2p --assume-yes
	dpkg-reconfigure i2p
fi
# build the macchanger boot script #####################################
#  changing the mac address at boot ensures connections appear from a
#  diffrent machine each time user reboots, this is not on a timer since
#  the interface needs brought down each time the mac is changed
if [ ! -f /usr/bin/macRandomizer ];then
	echo "#! /usr/bin/python" > /usr/bin/macRandomizer
	echo "from os import system"  > /usr/bin/macRandomizer
	echo "for index in range(51):\n" > /usr/bin/macRandomizer
	echo "\tsystem(('sudo macchanger --another eth'+str(index)))\n" > /usr/bin/macRandomizer
	echo "\tsystem(('sudo macchanger --another wlan'+str(index)))\n" > /usr/bin/macRandomizer
	chmod +x /usr/bin/macRandomizer
fi
# set macRandomizer to launch at boot though rc.local file
if more /etc/rc.local | grep macRandomizer;then
	sed -i "s/exit 0//g" /etc/rc.local
	echo "macRandomizer" >> /etc/rc.local
	echo "exit 0" >> /etc/rc.local
fi
########################################################################
# edit privoxy config to forward tor and i2p web links #################
# remove lines if they exist already
sed -i "s/forward-socks4a \/ localhost\:9050 .//g" /etc/privoxy/config
sed -i "s/forward .i2p localhost:4444//g" /etc/privoxy/config
# add lines to end of file
echo 'forward-socks4a / localhost:9050 .' >> /etc/privoxy/config
echo 'forward .i2p localhost:4444' >> /etc/privoxy/config
# remove logging by privoxy done by default to improve security
sed -i "s/logfile logfile//g" /etc/privoxy/config
# restart privoxy for changes to take place
service privoxy restart
echo 'Install of Tor, I2P, and privoxy, you now have access to the deepweb!'
echo 'To make anything go though tor set the proxy server ip to ::1 and the port to 8118'
