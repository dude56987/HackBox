#! /bin/bash
##############################################
# A script to setup login for a low ram system
##############################################
# Check ram to dertermine if it is a low ram system
memory=$(cat /proc/meminfo | grep MemTotal | sed "s/\ /\n/g" | grep [0987654321])
echo "$memory KB of total memory in the system..."
# memory is showm in kilobytes, current default is below 1.6 gigs
if [ "$memory" -lt 1600000 ];then
	echo "Setting low ram settings..."
	bash lxde-desktop.sh
	bash disable-bootsplash.sh
else
	echo "Installing preload..."
	# If more memory exists install the preload package to
	# speed up application startup by preloading applications
	# into ram
	sudo apt-get install preload --assume-yes >> /opt/hackbox/Install_Log.txt
fi
