#! /bin/bash
##########################################################################
# Setup hackbox setup relay server, this will feed out the torrent files #
##########################################################################
if [ "$(id -u)" != "0" ];then
	# check if script is being ran as root
	echo "This script must be run as root!"
	exit 1
fi
##########################################################################
# the relay will requrire an apache server
apt-get install apache2 --assume-yes
# open the webserver ports
ufw allow from any to any port 80
# create a relay section on the webserver
mkdir -p /var/www/html/hackbox-relay/
# create a global hostname variable for use in script
serverName=$(hostname)
# pull the server ip address since aria2c cant resolve mdns
ipAddress=$(arp -n $serverName'.local' | tr -d '()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'| tr -d '\-' | sed "s/\. //g")
###########################
# connect-to-relay script #
###########################
#This script is placed on the server to aid in setup of local machines.
echo "#! /bin/bash" > /var/www/html/hackbox-relay/connect-to-relay.sh
echo "echo $ipAddress > /etc/hackbox/relayServer" > /var/www/html/hackbox-relay/connect-to-relay.sh
echo "chmod go-rwx /etc/hackbox/relayServer" > /var/www/html/hackbox-relay/connect-to-relay.sh
chmod +x /var/www/html/hackbox-relay/connect-to-relay.sh
###############################################
# create a build system to run on cron for CI #
###############################################
cp -f /opt/hackbox/scripts/relayScripts/server-update-relay.sh /etc/cron.daily/00-hackbox-server-update-relay
# make the script execute
chmod +x /etc/cron.daily/00-hackbox-server-update-relay
# launch a relay server update to instantly startup the relay server
bash /etc/cron.daily/00-hackbox-server-update-relay

