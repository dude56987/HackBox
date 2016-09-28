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
####################################################################
# Install custom fonts for all users on system
########################################################################
# copy all fonts stored in the fonts directory into the system fonts directory
cp /opt/hackbox/media/fonts/*.otf /usr/share/fonts/truetype/ >> /opt/hackbox/Install_Log.txt
cp /opt/hackbox/media/fonts/*.ttf /usr/share/fonts/truetype/ >> /opt/hackbox/Install_Log.txt
# Refresh the font cache in order to make the system recognize the new fonts
fc-cache -f -v >> /opt/hackbox/Install_Log.txt
