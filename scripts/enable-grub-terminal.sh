#! /bin/bash
# This will set grub to startup completely in text mode, this makes boot much
# faster and will work on a wider variety of hardware.
if more /etc/default/grub | grep \#GRUB_TERMINAL ;then
	sudo sed -i -e 's/#GRUB_TERMINAL/GRUB_TERMINAL/g' /etc/default/grub
	sudo update-grub
fi
