#! /bin/bash
########################################################################
# Detect if system is a laptop and setup laptop settings
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
echo "Running laptop check script..."
if which laptop-detect;then
	echo "laptop-detect found on system :D"	
else
	echo "Installing laptop-detect..."
	sudo apt-get install laptop-detect --assume-yes
fi
echo "Checking if the running system is a laptop..."
if laptop-detect;then
	echo "System is a laptop, configuring system..."
	# install tlp (improves battery life in laptops)
	sudo apt-get install tlp --assume-yes
	# start tlp
	sudo tlp start
	# install fdpowermon battery indicator
	sudo apt-get install fdpowermon --assume-yes
	# install powertop top but for power management
	sudo apt-get install powertop --assume-yes
	# create a powertop autotune script to run on boot
	echo "$(which powertop) --auto-tune" > /etc/rc.local.d/powertop
else
	echo "Running system is not a laptop. End of program."
fi
