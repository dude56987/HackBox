#! /bin/bash
# Set custom grub splash screen and change grub timeout to 2 seconds
# move the .jpg file from the local media folder to /boot/grub/
cp media/splash.jpg /boot/grub/splash.jpg
if ! more /etc/default/grub | grep 'GRUB_TIMEOUT="2"';then
	# edit the grub settings to make the timeout 2 seconds insted of 5 for faster boot
	sed -i -e 's/^GRUB_TIMEOUT=.*$/GRUB_TIMEOUT="2"/g' /etc/default/grub
fi
# run sudo update-grub to make grub regonize the new splash image
sudo update-grub
