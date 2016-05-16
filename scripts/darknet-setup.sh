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
if ! [ -f /etc/hackbox/i2pSetupDone ];then
	# setting up i2p deepweb protocall though ppa ##########################
	# set anwsers for setup dialouges
	echo "i2p	i2p/user	string	i2psvc" > /tmp/i2p.conf
	echo "i2p	i2p/memory	string	128" >> /tmp/i2p.conf
	echo "i2p	i2p/daemon	boolean	true" >> /tmp/i2p.conf
	debconf-set-selections /tmp/i2p.conf
	# add ppa update and install program
	apt-add-repository ppa:i2p-maintainers/i2p --yes
	apt-get update
	apt-get install i2p --assume-yes
	dpkg-reconfigure i2p
	# create lock file so this process is not repeated
	echo '' > /etc/hackbox/i2pSetupDone
fi
########################################################################
# edit privoxy config to forward tor and i2p web links #################
# remove lines if they exist already and add lines to end of file
# first forward all traffic though tor
sed -i "s/forward-socks4a \/ localhost\:9050 .//g" /etc/privoxy/config
echo 'forward-socks4a / localhost:9050 .' >> /etc/privoxy/config
# forward all i2p requests to the i2p router
sed -i "s/forward .i2p localhost:4444//g" /etc/privoxy/config
echo 'forward .i2p localhost:4444' >> /etc/privoxy/config
# forward all requests to localhost back to localhost
sed -i "s/forward localhost\/ .//g" /etc/privoxy/config
echo 'forward localhost/ .' >> /etc/privoxy/config
sed -i "s/forward 127.0.0.1\/ .//g" /etc/privoxy/config
echo 'forward 127.0.0.1/ .' >> /etc/privoxy/config
# send any .local domains to the local lan
sed -i "s/forward .local .//g" /etc/privoxy/config
echo 'forward .local .' >> /etc/privoxy/config
# remove blank lines
sed -i '/^$/d' /etc/privoxy/config
# remove logging by privoxy done by default to improve security
sed -i "s/logfile logfile//g" /etc/privoxy/config
# restart privoxy for changes to take place
service privoxy restart
echo 'Install of Tor, I2P, and privoxy, you now have access to the deepweb!'
echo 'To make anything go though tor set the proxy server ip to ::1 and the port to 8118'
