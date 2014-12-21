#! /bin/bash
# disable screenblanking in tty
if more /etc/default/grub | grep "#GRUB_CMDLINE_LINUX_DEFAULT";then
	sudo sed -i -e 's/#GRUB_CMDLINE_LINUX_DEFAULT/GRUB_CMDLINE_LINUX_DEFAULT/g' /etc/default/grub
	while more /etc/default/grub | grep "##";do
		sudo sed -i -e 's/##/#/g' /etc/default/grub
	done
	sudo update-grub
fi
if ! more /etc/default/grub | grep "consoleblank=0";then
	# change line of boot to disable console blanking
	sudo sed -i -e 's/^GRUB_CMDLINE_LINUX_DEFAULT.*$/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash consoleblank=0"/g' /etc/default/grub
	# remove blanklines
	sudo sed -i '/^$/d' /etc/default/grub
	# update grub config
	sudo update-grub
fi
