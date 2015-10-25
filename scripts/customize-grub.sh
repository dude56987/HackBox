#! /bin/bash
########################################################################
# Customize the grub boot menu
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
# Set custom grub splash screen and change grub timeout to 2 seconds
# move the .jpg file from the local media folder to /boot/grub/
cp /opt/hackbox/media/splash.jpg /boot/grub/splash.jpg
if ! more /etc/default/grub | grep 'GRUB_TIMEOUT="2"';then
	# edit the grub settings to make the timeout 2 seconds instead of 5 for faster boot
	sed -i -e 's/^GRUB_TIMEOUT=.*$/GRUB_TIMEOUT="2"/g' /etc/default/grub
fi
if more /etc/default/grub | grep 'GRUB_HIDDEN';then
	# delete lines to hide grub on boot,since above we set the delay to 2 to show it
	sed -i -e 's/^GRUB_HIDDEN.*$//g' /etc/default/grub
fi
# remove blanklines
sed -i '/^$/d' /etc/default/grub
# run sudo update-grub to make grub regonize the new splash image
update-grub
