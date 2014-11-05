#! /bin/bash
##############################################
# A script to setup lxde as the desktop
##############################################
echo 'Setting up system for low ram pc...'
# add lxde desktop for low ram pcs and other lighter software
apt-get install lxde --assume-yes
apt-get install lxpanel-indicator-applet-plugin --assume-yes
apt-get install midori --assume-yes
apt-get install wicd-gtk --assume-yes
# purge login managers	
apt-get purge xdm --assume-yes
apt-get purge slim --assume-yes
apt-get purge mdm --assume-yes
apt-get purge gdm --assume-yes
apt-get purge lightdm --assume-yes
apt-get purge wdm --assume-yes
apt-get purge kdm --assume-yes
# change the virtual terminal to tty2 on boot
# this is because some systems output to tty1
# and default to it for the users input
sed -i "s/exit 0//g" /etc/rc.local
sed -i "s/chvt 2//g" /etc/rc.local
echo 'chvt 2' >> /etc/rc.local
echo 'exit 0' >> /etc/rc.local
#modify the configs in /etc/skel
sed -i "s/Session=*\n/Session=LXDE\n/g" /etc/skel/.dmrc
echo 'lxsession' > /etc/skel/.xinitrc
# edit the default extra groups users are added to when new users are made
echo 'EXTRA_GROUPS="audio netdev"' >> /etc/useradd.conf
echo 'ADD_EXTRA_GROUPS=1' >> /etc/useradd.conf
# modify existing users
for dir in /home/*;do
	USERNAME=$(echo $dir | sed "s/\/home\///g")
	# give some output to let the user know stuff is working right
	echo "Username:"
	echo $USERNAME
	echo "Editing $dir/.dmrc ..."
	sed -i "s/Session=*\n/Session=LXDE\n/g" $dir/.dmrc
	chown $USERNAME $dir/.dmrc
	# for antix/debian compatibility
	echo 'lxsession' > $dir/.xinitrc
	chown $USERNAME $dir/.xinitrc
	# give all users permissions for the audio group
	echo "usermod -a audio $USERNAME"
	usermod -a -G audio $USERNAME
	echo "usermod -a netdev $USERNAME"
	usermod -a -G netdev $USERNAME
done
