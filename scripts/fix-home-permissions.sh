########################################################################
# Make each users home directory private
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
# make home directories only readable by thier owners
echo "Changing the permissions of existing users..."
chmod --recursive u+rwX,g-rwx,o-rwx /home/*
# make the above the default for new users
echo "Changing the default permissions of new users..."
sed -i "s/DIR_MODE=[0987654321]\{1,4\}/DIR_MODE=0700/g" /etc/adduser.conf
grep "DIR_MODE=" /etc/adduser.conf
