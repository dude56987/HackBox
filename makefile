########################################################################
# Makefile for ubuntuSetup
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
all: batman
	echo 'This is the default run that builds and installs the program as a package. Everything should be installed if your seeing this.'
	echo 'When you log out and back in the installer will run automaticly in graphics mode.'
install : batman
	echo 'END OF LINE'
installtosystem:
	mkdir /opt/hackbox
	cp -vr * /opt/hackbox
	echo "#! /bin/bash\npython /opt/hackbox/hackboxsetup.py" > /usr/bin/hackboxsetup
	sudo chmod +x /usr/bin/hackboxsetup
	sudo chmod -Rv ugo+r /opt/hackbox/media/
uninstallfromsystem:
	rm -rv -v /opt/hackbox
	rm -rv /usr/bin/hackboxsetup
install-deb: hackbox_UNSTABLE.deb
	sudo gdebi --no hackbox_UNSTABLE.deb
build: 
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/opt;
	mkdir -p debian/opt/hackbox;
	mkdir -p debian/opt/hackbox/sources;
	mkdir -p debian/opt/hackbox/media;
	mkdir -p debian/opt/hackbox/preconfiguredSettings;
	mkdir -p debian/usr/share;
	mkdir -p debian/usr/share/applications;
	mkdir -p debian/usr/share/pixmaps;
	# make post and pre install scripts have the correct permissions
	chmod 775 .debdata/*
	# copy over the launcher for the program
	cp -vf media/launchers/HackBoxSetup.desktop debian/usr/share/applications/
	# copy over icons for the launchers
	cp -vf media/hackboxLogo.png debian/usr/share/pixmaps/
	# copy over the binary
	cp -vf hackboxsetup.py ./debian/opt/hackbox/hackboxsetup.py
	cp -vf hackboxsetup-gui.py ./debian/opt/hackbox/hackboxsetup-gui.py
	# build the launchers link
	echo "#! /bin/bash\npython /opt/hackbox/hackboxsetup.py" > ./debian/usr/bin/hackboxsetup
	chmod +x ./debian/usr/bin/hackboxsetup
	echo "#! /bin/bash\npython /opt/hackbox/hackboxsetup-gui.py" > ./debian/usr/bin/hackboxsetup-gui
	chmod +x ./debian/usr/bin/hackboxsetup-gui
	# give everyone read permissions for the media directory of hackbox
	chmod -Rv ugo+r ./debian/opt/hackbox/media/.
	# compress the preconfigured settings files
	# escape the endings to cd works since each line is executed as a separate process
	cd preconfiguredSettings/topBar/;\
	ls -A | zip -g -9 -r ../../debian/opt/hackbox/preconfiguredSettings/preconfiguredSettings.zip -@;
	# each line is executed as a separate process so it pops back to the main directory
	cd preconfiguredSettings/bottomBar/;\
	ls -A | zip -g -9 -r ../../debian/opt/hackbox/preconfiguredSettings/preconfiguredSettings_Bottom.zip -@;
	# add config files n such
	cp -vfr ./preconfiguredSettings/launchers ./debian/opt/hackbox/preconfiguredSettings/
	cp -vfr ./media/. ./debian/opt/hackbox/media/
	cp -vfr ./sources/. ./debian/opt/hackbox/sources/
	cp -vfr ./unsupportedPackages/. ./debian/opt/hackbox/unsupportedPackages/
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i.bak 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i.bak 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	# copy over the debdata files
	cp -rv .debdata/. debian/DEBIAN/
	# figure out the size of the installed package and save the size in kb to a file
	du -sx --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.]//g" > packageSize.txt
	# Attempt to auto set the size of the package in the control file ##CURRENTLY BROKEN##
	#~ bash -c '\
	#~ VALUE=$(du -s --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.\\t]\{1,\}//g");\
	#~ sed -i.bak "s/Installed-Size: [0123456789]\{2,20\}/Installed-Size: ${VALUE}/g" ./debian/DEBIAN/control;\
	#~ rm ./debian/DEBIAN/control.bak;\
	#~ ';
	# clear up backups from sed operations
	rm -v ./debian/DEBIAN/md5sums.bak
	chmod -R 775 ./debian/DEBIAN
	chmod -Rv ugo+r ./debian/opt/hackbox/media
	chmod -Rv ugo+x ./debian/opt/hackbox/media/launchers
	dpkg-deb --build debian
	cp -v debian.deb hackbox_UNSTABLE.deb
	# cleanup of unnamed package and package build folder
	rm -v debian.deb
	rm -rv debian
distro-build-env-setup:
	# install uck so distro can be built
	sudo apt-get install uck libfribidi-bin
	# second package is required in uck but not set as a dependency in uck package
	echo 'Done!'
distro-build:
	uck-gui
batman: build install-deb
	echo 'I am the Night.'
pullCustomSoftware: 
	mkdir -p customSoftwarePackages
	git clone https://github.com/dude56987/Distro-Upgrade.git customSoftwarePackages/distro-upgrade
	git clone https://github.com/dude56987/Reboot-Required.git customSoftwarePackages/reboot-required
	git clone https://github.com/dude56987/LanScan.git customSoftwarePackages/lanscan
	git clone https://github.com/dude56987/DoThis.git customSoftwarePackages/dothis
	git clone https://github.com/dude56987/Bitmessage-Update.git customSoftwarePackages/bitmessage-update
	git clone https://github.com/dude56987/HackBox-Update.git customSoftwarePackages/hackbox-update
	git clone https://github.com/dude56987/ResetSettings.git customSoftwarePackages/resetsettings
	git clone https://github.com/dude56987/Help-Center.git customSoftwarePackages/help-center
	git clone https://github.com/dude56987/OpenNIC-DNS.git customSoftwarePackages/opennic-dns
fix-permissions:
	# run all commands with sudo or it will fail
	# read allowed for all files and all users
	sudo chmod -R ugo+r *
	# remove write and execute for all files
	sudo chmod -R ugo-wx *
	# user has write permissions on all files
	sudo chmod -R u+w *
	# execute and read directories allowed for everyone
	sudo find . -type d -exec chmod +rx {} \;
#uninstall : uninstall.py
#	python uninstall.py
