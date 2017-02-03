#! /bin/bash
########################################################################
# Script to customize the grub boot options
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
# Other available boot options
# - Enable splashscreen
#   - "splash"
#   - Used to enable the grub splashscreen
########################################################################
# Set boot options to...
# - Disable screenblanking in tty
#   - "consoleblank=0"
#   - This annoys the shit out of people
# - Quiet boot
#   - "quiet"
#   - Boot faster
# - Disable perdictable network names
#   - "net.ifnames=0 biosdevname=0"
#   - This makes it work like legacy, e.g. with eth0, wlan0, eth1, wlan1, etc.
#     This should work perfectly for 99% of the people. Complex network card
#     configurations are not what the default settings should address.
# the line to be stubstuted, to add more options change the below line
subLine='GRUB_CMDLINE_LINUX_DEFAULT="quiet consoleblank=0 net.ifnames=0 biosdevname=0"'
#subLine='GRUB_CMDLINE_LINUX_DEFAULT="quiet consoleblank=0 biosdevname=0"'
#subLine='GRUB_CMDLINE_LINUX_DEFAULT="quiet consoleblank=0"'
if ! cat /etc/default/grub | grep "$subLine";then
	# uncomment the grub commandline options if they are commented out
	sed -i -e 's/#GRUB_CMDLINE_LINUX_DEFAULT/GRUB_CMDLINE_LINUX_DEFAULT/g' /etc/default/grub
	# change line of boot to disable console blanking
	sed -i -e "s/^GRUB_CMDLINE_LINUX_DEFAULT.*$/$subLine/g" /etc/default/grub
	# remove blanklines
	sed -i '/^$/d' /etc/default/grub
	# update grub config
	update-grub
fi
# install biosdevname if it is not already on the system
apt-get install biosdevname --assume-yes
