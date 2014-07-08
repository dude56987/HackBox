#! /bin/bash
# Check ram to dertermine if it is a low ram system
memory=$(cat /proc/meminfo | grep MemTotal | sed "s/\ /\n/g" | grep [0987654321])
echo "$memory KB of total memory in the system..."
# memory is showm in kilobytes, current default is below 1.6 gigs
if [ "$memory" -lt 1600000 ];then
	echo 'Setting up system for low ram pc...'
	apt-get install fluxbox --assume-yes
	apt-get install nitrogen --assume-yes
	apt-get install midori --assume-yes
	# copy over the style for fluxbox to use
	cp /opt/hackbox/media/themes/HackBox_Fluxbox /usr/share/fluxbox/styles/
	#modify the configs in /etc/skel
	sed -i "s/Session=*\n/Session=fluxbox\n/g" /etc/skel/.dmrc
	sed -i "s/DEFAULT_DESKTOP=\".*\"/DEFAULT_DESKTOP=\"fluxbox\"/g" /etc/skel/.xinitrc
	# modify existing users
	for dir in /home/*;do
		echo "Editing $dir/.dmrc ..."
		sed -i "s/Session=*\n/Session=fluxbox\n/g" $dir/.dmrc
		chown $(echo \$dir | sed \"s/\/home\///g\") $dir/.dmrc
		# for antix debian compatibility
		sed -i "s/DEFAULT_DESKTOP=\".*\"/DEFAULT_DESKTOP=\"fluxbox\"/g" $dir/.xinitrc
		chown $(echo \$dir | sed \"s/\/home\///g\") $dir/.xinitrc
	done
fi
