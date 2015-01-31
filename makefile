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
	sudo apt-get install gdebi --assume-yes
	sudo gdebi --no hackbox_UNSTABLE.deb
update-version-number:
	#^Version:.\{4\}[0987654321]\{1,20\}
	#VERSION-NUMBER=${git log --pretty=oneline --all | wc -l};echo $VERSION-NUMBER;
	#bash -c 'cat .debdata/control | sed "s/Version\: ....[0987654321]\{1,20\}/"$(git log --pretty=oneline --all | wc -l)"/g"'
	#bash -c 'cat .debdata/control | sed "s/Version\: 0\.5\.[0987654321]\{1,20\}/Version: 0.5."$(git log --pretty=oneline --all | wc -l)"/g"'
	cat .debdata/control | sed "s/Version\: 0\.5\.[0987654321]\{1,20\}/Version: 0.5."$(git log --pretty=oneline --all | wc -l)"/g"
	#sed -i -e "s/Version\: ....[0987654321]\{1,20\}/${VERSION-NUMBER}/g" .debdata/control
	# check changes
#	less .debdata/control
	# fix it back
#	cp .debdata/control.backup .debdata/control
update-relay: 
	# copy current directory to the relay directory
	# If a relay is setup this will update the package pushed
	# when the cron job is next run.
	sudo cp -rv * /opt/hackbox/update
	sudo bash /etc/cron.daily/00-hackbox-server-update-relay
build: 
	# build the deb
	sudo make build-deb;
build-deb:
	mkdir -p debian;
	mkdir -p debian/DEBIAN;
	mkdir -p debian/usr;
	mkdir -p debian/usr/bin;
	mkdir -p debian/opt;
	mkdir -p debian/opt/hackbox;
	mkdir -p debian/opt/hackbox/update;
	mkdir -p debian/opt/hackbox/sources;
	mkdir -p debian/opt/hackbox/media;
	mkdir -p debian/opt/hackbox/scripts;
	mkdir -p debian/opt/hackbox/preconfiguredSettings;
	mkdir -p debian/opt/hackbox/preconfiguredSettings/userSettings;
	mkdir -p debian/opt/hackbox/preconfiguredSettings/debconf;
	mkdir -p debian/usr/share;
	mkdir -p debian/usr/hackbox;
	mkdir -p debian/usr/share/applications;
	mkdir -p debian/usr/share/pixmaps;
	mkdir -p debian/etc;
	mkdir -p debian/etc/hackbox;
	mkdir -p debian/etc/hackbox/sources;
	# make post and pre install scripts have the correct permissions
	chmod 775 .debdata/*
	# copy over the launcher for the program
	cp -vf media/launchers/*.desktop debian/usr/share/applications/
	# copy over icons for the launchers
	cp -vf media/hackboxLogo.png debian/usr/share/pixmaps/
	# compile and copy over the binary files
	pycompile *.py
	cp -vf hackboxsetup.py ./debian/opt/hackbox/hackboxsetup.py
	cp -vf hackboxlib.py ./debian/opt/hackbox/hackboxlib.py
	cp -vf hackboxsetup-gui.py ./debian/opt/hackbox/hackboxsetup-gui.py
	# clean up those bytecode files
	rm -vf *.pyc
	# build the launchers link
	#echo "#! /bin/bash\npython /opt/hackbox/hackboxsetup.py" > ./debian/usr/bin/hackboxsetup
	#chmod +x ./debian/usr/bin/hackboxsetup
	echo "#! /bin/bash\npython /opt/hackbox/hackboxsetup-gui.py" > ./debian/usr/bin/hackboxsetup-gui
	chmod +x ./debian/usr/bin/hackboxsetup-gui
	# give everyone read permissions for the media directory of hackbox
	chmod -Rv ugo+r ./debian/opt/hackbox/media/.
	# compress the preconfigured settings files
	# escape the endings to cd works since each line is executed as a separate process
	cd preconfiguredSettings/userSettings/topBar/;\
	ls -A | zip -g -9 -r ../../../debian/opt/hackbox/preconfiguredSettings/userSettings/topBar.zip -@;
	# each line is executed as a separate process so it pops back to the main directory
	cd preconfiguredSettings/userSettings/bottomBar/;\
	ls -A | zip -g -9 -r ../../../debian/opt/hackbox/preconfiguredSettings/userSettings/bottomBar.zip -@;
	# add core settings
	cd preconfiguredSettings/userSettings/CORE/;\
	ls -A | zip -g -9 -r ../../../debian/opt/hackbox/preconfiguredSettings/userSettings/CORE.zip -@;
	# add config files n such
	cp -vfr ./preconfiguredSettings/launchers ./debian/opt/hackbox/preconfiguredSettings/
	cp -vfr ./preconfiguredSettings/debconf ./debian/opt/hackbox/preconfiguredSettings/
	cp -vfr ./preconfiguredSettings/launchers/applications/. ./debian/usr/share/applications/
	cp -vfr ./media/. ./debian/opt/hackbox/media/
	cp -vfr ./scripts/. ./debian/opt/hackbox/scripts/
	cp -vfr ./sources/. ./debian/opt/hackbox/sources/
	cp -vfr ./unsupportedPackages/. ./debian/opt/hackbox/unsupportedPackages/
	# copy over the relay server info if a relay has been setup
	cp -vf /etc/hackbox/relayServer ./debian/etc/hackbox/relayServer || echo 'WARNING:No relay server setup!'
	# Create the md5sums file
	find ./debian/ -type f -print0 | xargs -0 md5sum > ./debian/DEBIAN/md5sums
	# cut filenames of extra junk
	sed -i 's/\.\/debian\///g' ./debian/DEBIAN/md5sums
	sed -i 's/\\n*DEBIAN*\\n//g' ./debian/DEBIAN/md5sums
	sed -i 's/\\n*DEBIAN*//g' ./debian/DEBIAN/md5sums
	# copy over the debdata files
	cp -rv .debdata/. debian/DEBIAN/
	# figure out the size of the installed package and save the size in kb to a file
	du -sx --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.]//g" | tr -d "\n" | tr -d "\r" | sed "s/ //g" | sed "s/\t//g" > packageSize.txt
	# run bash script to edit the control file of the package
	bash .configure.sh
	# Attempt to auto set the size of the package in the control file ##CURRENTLY BROKEN##
	#~ bash -c '\
	#~ VALUE=$(du -s --exclude DEBIAN ./debian/ | sed "s/[abcdefghijklmnopqrstuvwxyz\ /.\\t]\{1,\}//g");\
	#~ sed -i.bak "s/Installed-Size: [0123456789]\{2,20\}/Installed-Size: ${VALUE}/g" ./debian/DEBIAN/control;\
	#~ rm ./debian/DEBIAN/control.bak;\
	#~ ';
	# set permissions correctly on things
	chmod -R 775 ./debian/DEBIAN
	chmod -Rv ugo+r ./debian/opt/hackbox/media
	chmod -Rv ugo+x ./debian/opt/hackbox/media/launchers
	dpkg-deb --build debian
	mv -vf debian.deb hackbox_UNSTABLE.deb
	# cleanup package build folder
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
	git clone https://github.com/dude56987/Distro-Upgrade.git customSoftwarePackages/distro-upgrade ||\
	git -C customSoftwarePackages/distro-upgrade pull
	git clone https://github.com/dude56987/Reboot-Required.git customSoftwarePackages/reboot-required ||\
	git -C customSoftwarePackages/reboot-required pull
	git clone https://github.com/dude56987/LanScan.git customSoftwarePackages/lanscan ||\
	git -C customSoftwarePackages/lanscan pull
	git clone https://github.com/dude56987/DoThis.git customSoftwarePackages/dothis ||\
	git -C customSoftwarePackages/dothis pull
	git clone https://github.com/dude56987/Bitmessage-Update.git customSoftwarePackages/bitmessage-update ||\
	git -C customSoftwarePackages/bitmessage-update pull
	git clone https://github.com/dude56987/HackBox-Update.git customSoftwarePackages/hackbox-update ||\
	git -C customSoftwarePackages/hackbox-update pull
	git clone https://github.com/dude56987/ResetSettings.git customSoftwarePackages/resetsettings ||\
	git -C customSoftwarePackages/resetsettings pull
	git clone https://github.com/dude56987/Help-Center.git customSoftwarePackages/help-center ||\
	git -C customSoftwarePackages/help-center pull
	git clone https://github.com/dude56987/OpenNIC-DNS.git customSoftwarePackages/opennic-dns ||\
	git -C customSoftwarePackages/opennic-dns pull
	git clone https://github.com/dude56987/HostfileBlocklist.git customSoftwarePackages/hostfileblocklist ||\
	git -C customSoftwarePackages/hostfileblocklist pull
	git clone https://github.com/dude56987/DNS-Precache.git customSoftwarePackages/dns-precache ||\
	git -C customSoftwarePackages/dns-precache pull
	git clone https://github.com/dude56987/HackBox-Darknet.git customSoftwarePackages/hackbox-darknet ||\
	git -C customSoftwarePackages/hackbox-darknet pull
	git clone https://github.com/dude56987/HackBox-Mimetype-Defaults.git customSoftwarePackages/hackbox-mimetype-defaults ||\
	git -C customSoftwarePackages/hackbox-mimetype-defaults pull
	git clone https://github.com/dude56987/Geolocate.git customSoftwarePackages/geolocate ||\
	git -C customSoftwarePackages/geolocate pull
customSoftwareStatus: 
	git -C customSoftwarePackages/distro-upgrade status
	git -C customSoftwarePackages/reboot-required status
	git -C customSoftwarePackages/lanscan status
	git -C customSoftwarePackages/dothis status
	git -C customSoftwarePackages/bitmessage-update status
	git -C customSoftwarePackages/hackbox-update status
	git -C customSoftwarePackages/resetsettings status
	git -C customSoftwarePackages/help-center status
	git -C customSoftwarePackages/opennic-dns status
	git -C customSoftwarePackages/hostfileblocklist status
	git -C customSoftwarePackages/dns-precache status
	git -C customSoftwarePackages/hackbox-darknet status
	git -C customSoftwarePackages/hackbox-mimetype-defaults status
	git -C customSoftwarePackages/geolocate status
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
clean-logs:
	sudo rm -vf /opt/hackbox/Install_Log.txt
	sudo rm -vf Install_Log.txt
clean-preconfigured-settings:
	# clean up firefox config settings
	rm -vf preconfiguredSettings/*Bar/.mozilla/firefox/mwad0hks.default/bookmarkbackups/*.json
	rm -vf preconfiguredSettings/*Bar/.mozilla/firefox/mwad0hks.default/*.log
	rm -vf preconfiguredSettings/*Bar/.mozilla/firefox/Crash\ Reports/*
test: 
	# Strange syntax is strange because you need a return value of 0 
	# aka no errors for each line in a makefile or it will fail completely
	# and stop execution on the spot. Grep returns a error if no occurences
	# of the search are found. So it must be done this way to keep the
	# searches going.
	bash -c "more /opt/hackbox/Install_Log.txt | grep Error;exit 0"
	bash -c "more /opt/hackbox/Install_Log.txt | grep Err;exit 0"
	bash -c "more /opt/hackbox/Install_Log.txt | grep not\ found;exit 0"
debug-install-settings:
	sudo cp -rvf preconfiguredSettings/userSettings/CORE/. /etc/skel/
	sudo cp -rvf preconfiguredSettings/userSettings/bottomBar/. /etc/skel/
#uninstall : uninstall.py
#	python uninstall.py
