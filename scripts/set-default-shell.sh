#! /bin/bash
########################################################################
# Install custom fonts for all users on the system
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
#set the new shell to...
newShell=zsh
# find shell path
shellPath=$(which $newShell)
# set zsh to the default shell for new users
useradd -D -s $shellPath
# set zsh to default shell for current users
sed -i "s/sh/$newShell/g" /etc/passwd
sed -i "s/bash/$newShell/g" /etc/passwd
sed -i "s/zsh/$newShell/g" /etc/passwd
sed -i "s/fish/$newShell/g" /etc/passwd
sed -i "s/dash/$newShell/g" /etc/passwd
# use chsh for each user on the system 
for user in /home/*;do
	# change the shell path to the new shell
	chsh $user -s $shellPath
done
