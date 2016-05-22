#! /usr/bin/python3
########################################################################
# GUI for Hackbox Setup
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
import os, sys
# openvt launches a tty on terminal 12 and waits till setup script has finished
os.system('pkexec openvt -c 12 -s -w -l hackboxlauncher')
exit()
