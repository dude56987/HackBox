#! /bin/bash
################################################################################
# this is the cron script that will pull the updates daily from the relay server
################################################################################
if [ "$(id -u)" != "0" ];then
	# check if script is being ran as root
	echo "This script must be run as root!"
	exit 1
fi
################################################################################
#md5URL=$(echo "http://$(cat /etc/hackbox/relayServer)/hackbox-relay/relayimage.md5")
#aria2c --follow-torrent=false $md5URL -d /opt/hackbox/relayUpdate
# create a local md5sum of the file to compare to the remote one
#md5sum /opt/hackbox/relayUpdate/hackbox_UNSTABLE.deb > /opt/hackbox/relayUpdate/local.md5
# compare them, if the same exit
#if ! $(diff /opt/hackbox/relayUpdate/local.md5 /opt/hackbox/relayUpdate/relayimage.md5);then
#	exit
#fi
torrentURL=$(echo "http://$(cat /etc/hackbox/relayServer)/hackbox-relay/relayimage.torrent")
if 
# create a directory for relay based update if it dont exist yet
mkdir -p /opt/hackbox/relayUpdate/
echo "Clearing old packages from system..."
# remove package if it already exists
rm /opt/hackbox/relayUpdate/hackbox_UNSTABLE.deb
# remove old torrent if it exists
rm /opt/hackbox/relayUpdate/relayimage.torrent
# download the torrent file (this will use the ip address of the relay server)
# DO NOT ADD TRAILING / to -d option in aria2c, it will fuck up 
echo "Downloading the torrent from the relay server..."
aria2c --follow-torrent=false $torrentURL -d /opt/hackbox/relayUpdate
# download torrent data first, dont seed
# DO NOT ADD TRAILING / to -d option in aria2c, it will fuck up 
# --bt-enable-lpd is to allow peer discovery on the lan
echo "Downloading the torrent of the package..."
aria2c --bt-hash-check-seed=false --bt-enable-lpd=true --seed-time=0 /opt/hackbox/relayUpdate/relayimage.torrent -d /opt/hackbox/relayUpdate
# install the new hackbox package onto the computer
echo "Installing new packaged onto the system..."
dpkg -i /opt/hackbox/relayUpdate/hackbox_UNSTABLE.deb
# launch and install hackboxsetup after torrent has downloaded
echo "Installing new version of hackboxsetup..."
hackboxsetup --force-use-config 
# seed for 4 hours after upgrade is complete
# DO NOT ADD TRAILING / to -d option in aria2c, it will fuck up 
echo "Seeding the file for other peers for 4 hours..."
rm /opt/hackbox/relayUpdate/hackbox_UNSTABLE.deb
aria2c -c --bt-hash-check-seed=true --bt-enable-lpd=true --seed-time=240 /opt/hackbox/relayUpdate/relayimage.torrent -d /opt/hackbox/relayUpdate
