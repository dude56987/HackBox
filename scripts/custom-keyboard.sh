#! /bin/bash
########################################################################
# Set custom keyboard key rebindings
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
#####################################################################
# Make dpkg run without prompts, use default answers for all questions
export DEBIAN_FRONTEND=noninteractive
export DEBCONF_NONINTERACTIVE_SEEN=true
# set the caps lock to work as the escape key
if grep -q 'XKBOPTIONS=\"\"' /etc/default/keyboard; then
	sed -i 's/XKBOPTIONS=""/XKBOPTIONS="caps:escape"/g' /etc/default/keyboard
	dpkg-reconfigure keyboard-configuration
fi
