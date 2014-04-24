# Insert all user alias commands below this line and before the if statements
alias ls='ls --color=always' # this will color the output of ls
alias ll='ls -la' # This is shorthand to show hidden files and permissions
alias lol="espeak 'ha ha ha ha ha'" # Sometimes its good to have a sense of humor
alias gettowork="cd ~/HackBox/" # This is used by the dev of hackbox, remove it if you want
alias console-setup='sudo dpkg-reconfigure console-setup' # this will reconfigure the console allowing you to change the size,font and some other stuff
# check if the user is in a fullscreen terminal
if tty | grep tty1; then
	# check if the user is new and would like help
	if [ ! -f ~/.byobu/advanceduser ]; then
		# set byobu backend to screen for following stuff to work
		byobu-select-backend screen;
		# asks user for input
		echo "Would you like to view the help file? [y/n]: ";
		# read the user input into string variable
		read string; 
		if [ "$string" = "y" ]; then
			echo "Appending help file to launch with byobu...";
			echo "screen -t MENU pdmenu" > ~/.byobu/windows;
			echo "screen -t HELP bash -c 'less ~/.terminalHelpFile'" >> ~/.byobu/windows;
			echo "screen -t SHELL zsh" >> ~/.byobu/windows;
			sort -u ~/.byobu/windows -o ~/.byobu/windows;
			echo "select HELP" >> ~/.byobu/windows;
		fi
		if [ "$string" = "n" ]; then
			# write window setup file
			echo "screen -t MENU pdmenu" > ~/.byobu/windows;
			echo "screen -t SHELL zsh" >> ~/.byobu/windows;
			echo "select SHELL" >> ~/.byobu/windows;
			# check if the user wants to disable help menu forever
			echo "Never ask about help file again? [y/n]: ";
			read string2;
			if [ "$string2" = "y" ]; then
				# add the flag file that prevents this from running
				echo 'You are truly a supa hakka!' > ~/.byobu/advanceduser;
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
