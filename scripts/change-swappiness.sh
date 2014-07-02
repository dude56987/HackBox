#! /bin/bash
# change swap space setup
more /etc/sysctl.conf | grep swappiness 
if more /etc/sysctl.conf | grep swappiness ; then
	echo 'Nothing to be done...'
else
	echo 'Set swap to 15...'
	sudo bash -c "echo 'vm.swappiness = 15' >> /etc/sysctl.conf"	
fi
