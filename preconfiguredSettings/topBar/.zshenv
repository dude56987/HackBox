# Insert all user alias commands below this line and before the if statements
alias ls='ls --color=always' # this will color the output of ls
alias ll='ls -la' # This is shorthand to show hidden files and permissions
alias lll='ll | more' # ll but piped into more, for reading a very full directory and searching
alias lol="espeak 'ha ha ha ha ha'" # Sometimes its good to have a sense of humor
alias gettowork="cd ~/HackBox/" # This is used by the dev of hackbox, remove it if you want
alias pullhackboxsource="cd && git clone https://github.com/dude56987/HackBox.git && gettowork" # same as above
alias console-setup='sudo dpkg-reconfigure console-setup' # this will reconfigure the console allowing you to change the size,font and some other stuff
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
		# set byobu backend to screen for following stuff to work
		byobu-select-backend screen;
		# asks user for input
		echo "Would you like to view the help file? [y/n]: ";
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
			echo "Never ask about help file again? [y/n]: ";
			read userConfirmForever;
			if [ "$userConfirmForever" = "y" ]; then
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
