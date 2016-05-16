#! /bin/bash
########################################################################
# Script to create the message of the day
# Copyright (C) 2016  Carl J Smith
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
# add message of the day script to system startup for users
########################################################################
# add message of the day to the rc.local startup directory
echo 'message-of-the-day' > /etc/rc.local.d/message-of-the-day
# write the message of the day script
echo "#! /bin/bash" > /usr/bin/message-of-the-day
echo 'for dir in /home/*;do' >> /usr/bin/message-of-the-day
echo "echo \"Editing \$dir/.motd ...\"" >> /usr/bin/message-of-the-day
echo "fortune -a > \$dir/.motd" >> /usr/bin/message-of-the-day
echo "chown \$(echo \$dir | sed \"s/\/home\///g\") \$dir/.motd" >> /usr/bin/message-of-the-day
echo 'done' >> /usr/bin/message-of-the-day
chown root /usr/bin/message-of-the-day
chmod u+xr /usr/bin/message-of-the-day
chmod go-wx /usr/bin/message-of-the-day
chmod go+r /usr/bin/message-of-the-day
########################################################################
# copy over system motd scripts
########################################################################
cp -rvf /opt/hackbox/media/ttyTheme/update-motd.d/. /etc/update-motd.d/
# fix permissions on motd scripts
chmod +x /etc/update-motd.d/*
chmod o-r /etc/update-motd.d/*
chmod ug+r /etc/update-motd.d/*
chmod u+w /etc/update-motd.d/*
