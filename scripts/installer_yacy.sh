#! /bin/bash
########################################################################
# Install yacy on Debian or Ubuntu
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
# YACY is a distributed search tool, open http://localhost:8090 to view
########################################################################
# Create a souces file for the yacy repo
echo 'deb http://debian.yacy.net ./' > /etc/apt/sources.list.d/yacy.list 
# add the key for the repo
wget http://debian.yacy.net/yacy_orbiter_key.asc -O- | apt-key add -
apt-key advanced --keyserver pgp.net.nz --recv-keys 03D886E7
# update repos and install depends + yacy
apt-get update
# java 7 is sufficient, only a headless version is needed
apt-get install openjdk-7-jre-headless --assume-yes
apt-get install yacy --assume-yes
