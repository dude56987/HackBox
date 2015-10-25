#! /bin/bash
########################################################################
# Script to disable console blanking in TTY
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
# disable screenblanking in tty
if more /etc/default/grub | grep "#GRUB_CMDLINE_LINUX_DEFAULT";then
	sudo sed -i -e 's/#GRUB_CMDLINE_LINUX_DEFAULT/GRUB_CMDLINE_LINUX_DEFAULT/g' /etc/default/grub
	while more /etc/default/grub | grep "##";do
		sudo sed -i -e 's/##/#/g' /etc/default/grub
	done
	sudo update-grub
fi
if ! more /etc/default/grub | grep "consoleblank=0";then
	# change line of boot to disable console blanking
	sudo sed -i -e 's/^GRUB_CMDLINE_LINUX_DEFAULT.*$/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash consoleblank=0"/g' /etc/default/grub
	# remove blanklines
	sudo sed -i '/^$/d' /etc/default/grub
	# update grub config
	sudo update-grub
fi
