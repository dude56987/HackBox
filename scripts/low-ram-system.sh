#! /bin/bash
##############################################
# A script to setup login for a low ram system
##############################################
# Check ram to dertermine if it is a low ram system
memory=$(cat /proc/meminfo | grep MemTotal | sed "s/\ /\n/g" | grep [0987654321])
echo "$memory KB of total memory in the system..."
# memory is showm in kilobytes, current default is below 1.6 gigs
if [ "$memory" -lt 1600000 ];then
	echo 'Setting up system for low ram pc...'
	apt-get install lxde --assume-yes
	apt-get install midori --assume-yes
	# purge login managers	
	apt-get purge xdm --assume-yes
	apt-get purge mdm --assume-yes
	apt-get purge gdm --assume-yes
	apt-get purge lightdm --assume-yes
	apt-get purge wdm --assume-yes
	apt-get purge kdm --assume-yes
	#modify the configs in /etc/skel
	sed -i "s/Session=*\n/Session=LXDE\n/g" /etc/skel/.dmrc
	echo 'lxsession' > /etc/skel/.xinitrc
	# edit the default extra groups users are added to when new users are made
	echo 'EXTRA_GROUPS="audio"' >> /etc/useradd.conf
	echo 'ADD_EXTRA_GROUPS=1' >> /etc/useradd.conf
	# modify existing users
	for dir in /home/*;do
		echo "Editing $dir/.dmrc ..."
		sed -i "s/Session=*\n/Session=LXDE\n/g" $dir/.dmrc
		chown $(echo \$dir | sed \"s/\/home\///g\") $dir/.dmrc
		# for antix debian compatibility
		echo 'lxsession' > $dir/.xinitrc
		chown $(echo \$dir | sed \"s/\/home\///g\") $dir/.xinitrc
		# give all users permissions for the audio group
		usermod -a -G audio $(echo \$dir | sed \"s/\/home\///g\")
	done
fi
