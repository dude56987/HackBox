#! /bin/bash
# check if its a laptop
if more /etc/default/grub | grep \#GRUB_TERMINAL ;then
	sudo sed -i -e 's/#GRUB_TERMINAL/GRUB_TERMINAL/g' /etc/default/grub
	sudo update-grub
fi
