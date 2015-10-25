#! /bin/bash
###############################################################################
# Update the hackbox setup relay server, this will feed out the torrent files #
###############################################################################
if [ "$(id -u)" != "0" ];then
	# check if script is being ran as root
	echo "This script must be run as root!"
	exit 1
fi
###############################################
# figure out the hostname so we can get the ip address
serverName=$(hostname)
# pull the server ip address since aria2c cant resolve mdns
ipAddress=$(arp -n $serverName'.local' | tr -d '()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'| tr -d '\-' | sed "s/\. //g")
bash -c 'cd /opt/hackbox/update/;make build'
cp -vf /opt/hackbox/update/hackbox_UNSTABLE.deb /var/www/html/hackbox-relay/hackbox_UNSTABLE.deb
mkdir -p /var/www/html/hackbox-relay/
# create a md5sum for dertermining updates
md5sum /opt/hackbox/update/hackbox_UNSTABLE.deb > /var/www/html/hackbox-relay/relayimage.md5
# remove old torrent
rm -vf /var/www/html/hackbox-relay/relayimage.torrent
# create torrent file for clients to pull
mktorrent /var/www/html/hackbox-relay/hackbox_UNSTABLE.deb -o /var/www/html/hackbox-relay/relayimage.torrent -w "http://$ipAddress/hackbox-relay/hackbox_UNSTABLE.deb" -a "."
