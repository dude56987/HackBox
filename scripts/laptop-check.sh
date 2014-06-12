#! /bin/bash
# check if its a laptop
if laptop-detect;then
	# install laptop-mode-tools package
	sudo apt-get install laptop-mode-tools --assume-yes
	# enable laptop-mode-tools
	sudo laptop-mode
fi
