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
# check if its a laptop
if laptop-detect;then
	# install laptop-mode-tools package
	sudo apt-get install laptop-mode-tools --assume-yes
	# install fdpowermon battery indicator
	sudo apt-get install fdpowermon --assume-yes
	# enable laptop-mode-tools
	sudo laptop-mode
fi
