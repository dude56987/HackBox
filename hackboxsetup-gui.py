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
# launch the program on xterm
if os.path.exists('/usr/bin/xterm') == False:
	# if xterm is not installed, then install it
	os.system('gksu "apt-get install xterm --assume-yes"')
	os.system('gksu "apt-get install screen --assume-yes"')
if ("--upgrade" in sys.argv):
	# if running an upgrade
	print("Running a system upgrade...")
	os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfigUpgrade"')
else:
	# otherwise do default output
	os.system('xterm -maximized -T Hackbox\ Setup -e "screen -c /opt/hackbox/media/screenConfig/screenConfig"')
exit()
