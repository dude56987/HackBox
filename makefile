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
all:
	sudo make install 
	# This is the default run that builds and installs the program as a package. Everything should be installed if your seeing this.
	# When you log out and back in the installer will run automaticly in graphics mode.
install: build-deb install-deb
	echo 'END OF LINE'
installtosystem:
	mkdir /opt/hackbox
	cp -vr * /opt/hackbox
	echo "#! /bin/bash\npython3 /opt/hackbox/hackboxsetup.py" > /usr/bin/hackboxsetup
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
	# copy over HackBox icons for the launchers
	cp -vf media/hackboxLogo.png debian/usr/share/pixmaps/
	# compile and copy over the binary files
	pycompile *.py
	cp -vf hackboxsetup.py ./debian/opt/hackbox/hackboxsetup.py
	cp -vf hackboxlib.py ./debian/opt/hackbox/hackboxlib.py
	cp -vf hackboxgui.py ./debian/opt/hackbox/hackboxgui.py
	cp -vf hackboxsetup-gui.py ./debian/opt/hackbox/hackboxsetup-gui.py
	# clean up those bytecode files
	rm -vf *.pyc
	# give everyone read permissions for the media directory of hackbox
	chmod -Rv ugo+r ./debian/opt/hackbox/media/.
	# compress the preconfigured settings files
	# escape the endings to cd works since each line is executed as a separate process
	cp -rvf preconfiguredSettings/userSettings/* debian/opt/hackbox/preconfiguredSettings/userSettings/
	# fix permissions on usersettings
	chmod -R ugo-xw debian/opt/hackbox/preconfiguredSettings/userSettings/
	chmod -R ugo+rX debian/opt/hackbox/preconfiguredSettings/userSettings/
	chmod -R u+w debian/opt/hackbox/preconfiguredSettings/userSettings/
	# add config files n such
	cp -vfr ./preconfiguredSettings ./debian/opt/hackbox/
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
	# generate the changelog
	git log > ./debian/DEBIAN/changelog
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
build-deb: build
	# max compression on package
	dpkg-deb -Z xz -z 9 -S extreme --build debian
	mv -vf debian.deb hackbox_UNSTABLE.deb
	# cleanup package build folder
	rm -rv debian
test-builds: build
	# run compression strategys all at once to maximize core usage
	# max compression on package with xz compression
	dpkg-deb -Z xz -z 9 -S extreme --build debian && mv -vf debian.deb hackbox_UNSTABLE_xz.deb
	# max compression on package with lzma compression
	dpkg-deb -Z lzma -z 9 --build debian && mv -vf debian.deb hackbox_UNSTABLE_lzma.deb
	# max compression on package with bzip compression
	dpkg-deb -Z bzip2 -z 9 --build debian && mv -vf debian.deb hackbox_UNSTABLE_bzip.deb
	# max compression on package with gzip compression
	dpkg-deb -Z gzip -z 9 --build debian && mv -vf debian.deb hackbox_UNSTABLE_gzip.deb
distro-build-env-setup:
	# install uck so distro can be built
	#sudo apt-get install uck libfribidi-bin
	# live-build works uck is broken
	sudo apt-get install live-build
	# second package is required in uck but not set as a dependency in uck package
	echo 'Done!'
distro-build:
	mkdir distroBuild -p
	#uck-gui
	cd distroBuild && sudo lb config
	cd distroBuild && sudo lb build
	cd distroBuild && sudo lb config --mode ubuntu --distribution vivid --archive-areas "main multiverse vivid-backports universe contrib" --binary-images iso-hybrid --architecture i386 --debian-installer live 
	cd distroBuild && sudo lb build
	#cd distroBuild && lb config --mode ubuntu --distribution vivid --hostname livecd --username livecduser --archive-areas "main multiverse vivid-backports universe contrib" --binary-images iso-hybrid --architecture i386 --debian-installer livetman: build install-deb
	##############
pullCustomSoftware:
	mkdir -p customSoftwarePackages
	# project-report (generate project reports for git repositories)
	git clone https://github.com/dude56987/project-report.git customSoftwarePackages/project-report ||\
	git -C customSoftwarePackages/project-report pull
	# log-cleaner (manage cron job to clean out system logs on interval)
	git clone https://github.com/dude56987/log-cleaner.git customSoftwarePackages/log-cleaner ||\
	git -C customSoftwarePackages/log-cleaner pull
	# Hackbox System Monitor (Web frontend to munin and vnstati)
	git clone https://github.com/dude56987/hackbox-system-monitor.git customSoftwarePackages/hackbox-system-monitor ||\
	git -C customSoftwarePackages/hackbox-system-monitor pull
	# mkrd (GUI Ram Disk Tool)
	git clone https://github.com/dude56987/mkrd.git customSoftwarePackages/mkrd ||\
	git -C customSoftwarePackages/mkrd pull
	# redshiftRunner
	git clone https://github.com/dude56987/redshiftRunner.git customSoftwarePackages/redshiftrunner ||\
	git -C customSoftwarePackages/redshiftrunner pull
	# desktop layout picker
	git clone https://github.com/dude56987/Desktop-Layout-Picker.git customSoftwarePackages/desktop-layout-picker ||\
	git -C customSoftwarePackages/desktop-layout-picker pull
	# distro upgrade
	git clone https://github.com/dude56987/Distro-Upgrade.git customSoftwarePackages/distro-upgrade ||\
	git -C customSoftwarePackages/distro-upgrade pull
	# reboot-required
	git clone https://github.com/dude56987/Reboot-Required.git customSoftwarePackages/reboot-required ||\
	git -C customSoftwarePackages/reboot-required pull
	# lanscan
	git clone https://github.com/dude56987/LanScan.git customSoftwarePackages/lanscan ||\
	git -C customSoftwarePackages/lanscan pull
	# dothis
	git clone https://github.com/dude56987/DoThis.git customSoftwarePackages/dothis ||\
	git -C customSoftwarePackages/dothis pull
	# bitmessage update
	git clone https://github.com/dude56987/Bitmessage-Update.git customSoftwarePackages/bitmessage-update ||\
	git -C customSoftwarePackages/bitmessage-update pull
	# hackbox-update
	git clone https://github.com/dude56987/HackBox-Update.git customSoftwarePackages/hackbox-update ||\
	git -C customSoftwarePackages/hackbox-update pull
	# resetsettings
	git clone https://github.com/dude56987/ResetSettings.git customSoftwarePackages/resetsettings ||\
	git -C customSoftwarePackages/resetsettings pull
	# help-center
	git clone https://github.com/dude56987/Help-Center.git customSoftwarePackages/help-center ||\
	git -C customSoftwarePackages/help-center pull
	# opennic-dns
	git clone https://github.com/dude56987/OpenNIC-DNS.git customSoftwarePackages/opennic-dns ||\
	git -C customSoftwarePackages/opennic-dns pull
	# hostfileblocklist
	git clone https://github.com/dude56987/HostfileBlocklist.git customSoftwarePackages/hostfileblocklist ||\
	git -C customSoftwarePackages/hostfileblocklist pull
	# dns-precache
	git clone https://github.com/dude56987/DNS-Precache.git customSoftwarePackages/dns-precache ||\
	git -C customSoftwarePackages/dns-precache pull
	# hackbox-mimetypes
	git clone https://github.com/dude56987/HackBox-Mimetype-Defaults.git customSoftwarePackages/hackbox-mimetype-defaults ||\
	git -C customSoftwarePackages/hackbox-mimetype-defaults pull
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
	sudo chmod -R ugo+X *
clean-logs:
	sudo rm -vf /opt/hackbox/Install_Log.txt
	sudo rm -vf Install_Log.txt
getCurrentFirefoxSettings:
	# get bare minimum firefox settings of users current firefox profile
	#
	# remove existing firefox profile
	rm -rv preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/*
	# copy over the addons list
	cp -v ~/.mozilla/firefox/*.default/addons.json preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# user set preferences
	cp -v ~/.mozilla/firefox/*.default/prefs.js preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# this is a config that stores the extension list used by firefox
	cp -v ~/.mozilla/firefox/*.default/extensions.json preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# this is where the extension xpi files and data are stored
	cp -rv ~/.mozilla/firefox/*.default/extensions preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	cp -rv ~/.mozilla/firefox/*.default/extension-data preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# grab the configurations for the search plugins
	cp -v ~/.mozilla/firefox/*.default/search.json preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	cp -v ~/.mozilla/firefox/*.default/search-metadata.json preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	cp -rv ~/.mozilla/firefox/*.default/searchplugins preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# user agent switcher settings
	cp -rv ~/.mozilla/firefox/*.default/useragentswitcher preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# proxy selector settings
	cp -v ~/.mozilla/firefox/*.default/proxyselector.rdf preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# backup user styles stored by sylish
	cp -v ~/.mozilla/firefox/*.default/stylish.sqlite preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# get the bookmarks 
	cp -rv ~/.mozilla/firefox/*.default/bookmarkbackups preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
	# copy the settings for toolbar states
	cp -rv ~/.mozilla/firefox/*.default/xulstore.json preconfiguredSettings/userSettings/CORE/.mozilla/firefox/mwad0hks.default/
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
project-report: .git/*
	project-report --ignore customSoftwarePackages/ --ignore scripts/ --ignore hackboxsetup.py --ignore hackboxsetup-gui.py --trace /opt/hackbox/hackboxsetup.py --debug
