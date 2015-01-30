# Insert all user alias commands below this line and before the if statements
alias ls='ls --color=always' # this will color the output of ls
alias sl='ls' # fix the common typing mistake
alias l='ls' # fix the common typing mistake
alias ll='ls -la | more -d' # This is shorthand to show hidden files and permissions
alias c='clear' # Shorthand for clear screen
alias less='less -R' # Show colors when escape sequences for them are used 
alias grep='grep --color=auto' # colorize the output of grep
alias fgrep='fgrep --color=auto' # colorize the output of grep
alias egrep='egrep --color=auto' # colorize the output of grep
alias diff='colordiff' # colorize the output of diff
alias logview='tail -f /var/log/*' # View system log updates in realtime 
alias lol="espeak 'ha ha ha ha ha'" # Sometimes its good to have a sense of humor
alias say="espeak" # Speak the following string of text
alias ping="ping -c 5" # set default ping count to 5
alias system-info="inxi -F" # set default ping count to 5
alias root="sudo -s" # root logs into root mode for user
alias invert-color="xcalib -invert -alter" # Invert monitor colors
alias nightvision="export TERM=xterm-mono;unalias ls;prompt suse;xcalib -clear;xcalib -i -a;xcalib -green .1 0 1 -blue .1 0 1 -red 0.8 0 100 -alter"
# install some helpfull tools for working on a console only system
alias installConsoleTools='sudo apt-fast install fbgrab elinks links2 pianobar fbi wicd-curses weechat weechat-plugins weechat-scripts finch vlock'
alias installTerminalTools='installConsoleTools'
# this will reconfigure the console allowing you to change the size,font and some other stuff
alias console-setup='sudo dpkg-reconfigure console-setup'
alias terminal-setup='console-setup'
# downloads random wallpapers #BEWARE# truly random, stored in /usr/share/pixmaps/wallpapers
alias download-random-wallpapers="curl http://boards.4chan.org/wg/ | sed 's/\"/\n/g' | grep //i.4cdn.org/wg/ | sort -u | sed 's/\/\/i/http:\/\/i/g' > /tmp/images.list && sudo mkdir -p /usr/share/pixmaps/wallpapers && cd /usr/share/pixmaps/wallpapers && sudo wget -i /tmp/images.list && sudo fdupes -rdN /usr/share/pixmaps/wallpapers && cd"
alias download-random-anime-wallpapers="curl http://boards.4chan.org/w/ | sed 's/\"/\n/g' | grep //i.4cdn.org/w/ | sort -u | sed 's/\/\/i/http:\/\/i/g' > /tmp/images.list && sudo mkdir -p /usr/share/pixmaps/wallpapers && cd /usr/share/pixmaps/wallpapers && sudo wget -i /tmp/images.list && sudo fdupes -rdN /usr/share/pixmaps/wallpapers && cd"
alias download-random-quote-wallpapers="wget http://reddit.com/r/QuotesPorn/ -O /tmp/images.list && sed -i 's/\"/\n/g' /tmp/images.list && more /tmp/images.list | grep http://i.imgur.com/ > /tmp/images.final && sudo mkdir -p /usr/share/pixmaps/wallpapers && cd /usr/share/pixmaps/wallpapers && sudo wget -i /tmp/images.final && sudo fdupes -rdN /usr/share/pixmaps/wallpapers && cd"
# The rest of the commands are for use by the dev of hackbox, remove them if you want
alias gettowork="cd ~/Programming/HackBox/"
alias pullhackboxsource="mkdir -p ~/Programming/ && cd ~/Programming/ && git clone https://github.com/dude56987/HackBox.git && gettowork"
# run xset commands to keep the screen from blanking
xset s 0 0
xset s off
xset -dpms
setterm -blank 0
setterm -powersave off
setterm -powerdown 0
# clear the screen
clear;
# lulz, you need em sometimes
if date | grep Apr\ \ 1; then
	repeat 10 bash -c "echo 'killallhumans';sleep 1"
	echo 'erm.. uh.. Happy Birthday!' | cowsay -f tux
fi
####################################
# Auto mount remote locations on a ssh server to local filesystem
# remember to setup keys for this or you will be prompted for the password to the server on each login
#sshfs user@hostname.local:/home/user/Music ~/Music &
#sshfs user@hostname.local:/home/user/Documents ~/Documents &
#sshfs user@hostname.local:/home/user/Pictures ~/Pictures &
#sshfs user@hostname.local:/home/user/Videos ~/Videos &
#sshfs user@hostname.local:/home/user/Share ~/Share &
# Or just mount the entire remote home directory, Ive not tested this though it would probably end badly since you need this file in your home to run it on login
#sshfs user@hostname.local:/home/user/ ~/
####################################
# clear the screen again
clear;
# Show the user thier fortune for this login using cowsay
#  To change the theme used replace tux with one of the 
#  cowfiles listed by the command cowsay -l
more ~/.motd | cowsay -f none
# check if the user is in a fullscreen terminal
if tty | grep tty1 || tty | grep tty2 || tty | grep tty3 || tty | grep tty4; then
	# if Xorg is not running then launch a graphical window system
	if ! ps -e | grep Xorg; then
		if [ -f /usr/bin/startx ]; then
			# launch startx if it exists
			if startx; then
				# if start x worked correctly return true and exit
				exit;
			fi
			# if start x failed to work correctly this tree will exit and the terminal will launch
		fi
		# if x does not need started or does not exist then launch byobu
	fi
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
			sudo sed -i 's/XKBOPTIONS=""/XKBOPTIONS="caps:escape"/g' /etc/default/keyboard
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
