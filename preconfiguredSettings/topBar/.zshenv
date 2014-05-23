# Insert all user alias commands below this line and before the if statements
alias ls='ls --color=always' # this will color the output of ls
alias ll='ls -la | more -d' # This is shorthand to show hidden files and permissions
alias less='less -R' # Make the less command handle escape sequenced colors
alias lol="espeak 'ha ha ha ha ha'" # Sometimes its good to have a sense of humor
alias say="espeak" # Speak the following string of text
# install some helpfull tools for working on a console only system
alias installConsoleTools='sudo apt-fast install vlock fbgrab elinks links2 pianobar fbi wicd-curses weechat weechat-plugins weechat-scripts finch vlock' 
# this will reconfigure the console allowing you to change the size,font and some other stuff
alias console-setup='sudo dpkg-reconfigure console-setup'
# The rest of the commands are for use by the dev of hackbox, remove them if you want
alias gettowork="cd ~/HackBox/"
alias pullhackboxsource="cd && git clone https://github.com/dude56987/HackBox.git && gettowork"
# check if the user is in a fullscreen terminal
if tty | grep tty1; then
	# check where the byobu settings are being stored
	if [ -d .byobu/ ]; then
		configPath=".byobu/";
	elif [ -d .local/share/byobu ]; then
		configPath=".local/share/byobu/";
	fi
	echo "Config path set as ${configPath}"
	# check if the user is new and would like help
	if [ ! -f ${configPath}advanceduser ]; then
		# check if programs are installed for enviorment
		if [ ! -f /usr/bin/screen ]; then
			echo "Screen was not found!";
			echo "Please enter your password to install it...";
			sudo apt-get install screen --assume-yes;
		fi
		if [ ! -f /usr/bin/pdmenu ]; then
			echo "pdmenu was not found!";
			echo "Please enter your password to install it...";
			sudo apt-get install pdmenu --assume-yes;
		fi
		if [ ! -f /usr/bin/vlock ]; then
			echo "vlock was not found!";
			echo "Please enter your password to install it...";
			sudo apt-get install vlock --assume-yes;
		fi
		if locate libgpm | grep libgpm; then
			echo "gpm was not found!";
			echo "Please enter your password to install it...";
			sudo apt-get install gpm --assume-yes;
		fi
		# set the caps lock to work as the escape key
		if more /etc/default/keyboard | grep 'XKBOPTIONS=\"\"'; then
			sudo sed -i.bak 's/XKBOPTIONS=""/XKBOPTIONS="caps:escape"/g' /etc/default/keyboard
			sudo rm -v /etc/default/keyboard.bak
			sudo dpkg-reconfigure keyboard-configuration
		fi

		#set byobu backend to screen for following stuff to work
		byobu-select-backend screen;
		# asks user for input
		clear
		echo "=============================================================="
		echo "It has been detected that this is your first time using a TTY!"
		echo "=============================================================="
		echo "Would you like to view the help file to get you started? [y/n]: ";
		# read the user input into string variable
		read userAnwserString; 
		if [ "$userAnwserString" = "y" ]; then
			echo "Appending help file to launch with byobu...";
			echo "screen -t MENU pdmenu" > ${configPath}windows;
			echo "screen -t HELP bash -c 'less ~/.terminalHelpFile'" >> ${configPath}windows;
			echo "screen -t SHELL zsh" >> ${configPath}windows;
			sort -u ${configPath}windows -o ${configPath}windows;
			echo "select HELP" >> ${configPath}windows;
		else
			# write window setup file
			echo "screen -t MENU pdmenu" > ${configPath}windows;
			echo "screen -t SHELL zsh" >> ${configPath}windows;
			echo "select SHELL" >> ${configPath}windows;
			# check if the user wants to disable help menu forever
			echo "Ask about the help file next time? [y/n]: ";
			read userConfirmForever;
			if [ "$userConfirmForever" = "n" ]; then
				# add the flag file that prevents this from running
				echo 'You are truly a supa hakka!' > ${configPath}advanceduser;
				echo 'To view the help file at any time use the following command.';
				echo 'less ~/.terminalHelpFile';
				echo 'Press enter to proceed...';
				read;
			fi
		fi
	fi
	# launch byobu
	byobu;
	# exit when all terminals are closed
	exit;
fi
