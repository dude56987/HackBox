#! /bin/bash
#######################################################################
# A script to create a shutdown and reboot user. These users require no 
# password and only peform what they are called when used without a 
# interactive shell.
#######################################################################
# create shutdown user home directories
mkdir -p /etc/power-control-logins
mkdir -p /etc/power-control-logins/shutdown
mkdir -p /etc/power-control-logins/reboot
# create bash rc files to lauch on login for the power-control login accounts
echo "sudo shutdown -P 'now' &while true; do read;done" > /etc/power-control-logins/shutdown/.bash_login
echo "sudo reboot &while true; do read;done" > /etc/power-control-logins/reboot/.bash_login
# create a copy of the /etc/sudoers file for editing
cp /etc/sudoers /tmp/sudoers.tmp
# edit the sudoers file, if it has not already been edited
if ! more /tmp/sudoers.tmp | grep "shutdown ALL=(ALL) NOPASSWD:/sbin/shutdown"; then
	echo "shutdown ALL=(ALL) NOPASSWD:/sbin/shutdown" >> /tmp/sudoers.tmp
fi
if ! more /tmp/sudoers.tmp | grep "reboot ALL=(ALL) NOPASSWD:/sbin/reboot"; then
	echo "reboot ALL=(ALL) NOPASSWD:/sbin/reboot" >> /tmp/sudoers.tmp
fi
# check if changes to file are valid
if visudo -c -f /tmp/sudoers.tmp; then
	# copy over the edits to the sudoers file
	cp -v /tmp/sudoers.tmp /etc/sudoers
else
	echo '/etc/sudoers file edits failed!'
fi
# delete user if they exist to remake them
deluser shutdown
deluser reboot
# switch to useradd command as it requires less crap
useradd --system -M --no-user-group --home /etc/power-control-logins/shutdown/ --shell /bin/bash --password password shutdown
useradd --system -M --no-user-group --home /etc/power-control-logins/reboot/ --shell /bin/bash --password password reboot
# delete password and enable login for passwordless login to allow shutdown and reboot
passwd -d -u shutdown
passwd -d -u reboot
