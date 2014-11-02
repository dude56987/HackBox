#! /bin/bash
#######################################################################
# A script to make sudo show astrisk feedback when passwords are typed
#######################################################################
# create a copy of the /etc/sudoers file for editing
cp /etc/sudoers /tmp/sudoers.tmp
# edit the sudoers file, if it has not already been edited
if ! more /tmp/sudoers.tmp | grep "Defaults pwfeedback"; then
	echo "Defaults pwfeedback" >> /tmp/sudoers.tmp
fi
# check if changes to file are valid
if visudo -c -f /tmp/sudoers.tmp; then
	# copy over the edits to the sudoers file
	cp -v /tmp/sudoers.tmp /etc/sudoers
else
	echo '/etc/sudoers file edits failed!'
fi
# remove temp file
rm -fv /tmp/sudoers.tmp
