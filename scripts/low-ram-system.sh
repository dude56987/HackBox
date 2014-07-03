#! /bin/bash
# Check ram to dertermine if it is a low ram system
memory=$(cat /proc/meminfo | grep MemTotal | sed "s/\ /\n/g" | grep [0987654321])
echo "$memory KB of total memory in the system..."
# memory is showm in kilobytes, current default is below 2 gigs
if [ "$memory" -lt 2000000 ];then
	echo 'Setting up system for low ram pc...'
	apt-get install fluxbox --assume-yes
	apt-get install nitrogen --assume-yes
	sed -i "s/Session=*\n/Session=fluxbox\n/g" /etc/skel/.dmrc
	for dir in /home/*;do
		echo "Editing $dir/.dmrc ..."
		sed -i "s/Session=*\n/Session=fluxbox\n/g" $dir/.dmrc
	done
fi
