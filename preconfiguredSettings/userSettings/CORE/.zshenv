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
alias trash='trash -v' # add verbosity to the trash command
alias viewlogs='sudo lnav /var/log/' # View system log updates in realtime
alias cleanlogs='sudo find /var/log/ -type f -delete -print' # remove all stored system logs
alias lol="espeak 'ha ha ha ha ha'" # Sometimes its good to have a sense of humor
alias say="espeak" # Speak the following string of text
alias ping="ping -c 5" # set default ping count to 5
alias system-info="inxi -F" # set default ping count to 5
alias root="sudo -s" # root logs into root mode for user
alias pm="sudo aptitude" # shorthand to run a package manager command
alias fix-permissions='sudo chmod u+rwX -R ~/. && sudo chmod g-w -R ~/. && sudo chmod g+rX -R ~/. && sudo chmod o-rwx -R ~/. && sudo chown -R $USER ~/'
alias mugshot-gen='identicon -s 256 -t -H $(echo "$(whoami)@$(hostname)"| md5sum | sed "s/[\ ,-]//g") -o ~/.face'
alias invert-color="xcalib -invert -alter" # Invert monitor colors
alias nightvision="export TERM=xterm-mono;unalias ls;prompt suse;xcalib -clear;xcalib -i -a;xcalib -green .1 0 1 -blue .1 0 1 -red 0.8 0 100 -alter"
# install some helpfull tools for working on a console only system
alias installConsoleTools='sudo apt-fast install fbgrab elinks links2 pianobar fbi wicd-curses weechat weechat-plugins weechat-scripts finch vlock'
alias installTerminalTools='installConsoleTools'
# this will reconfigure the console allowing you to change the size,font and some other stuff
alias console-setup='sudo dpkg-reconfigure console-setup'
alias terminal-setup='console-setup'
# import functions file with larger more complex functions(stuff to big for aliases)
. ~/.bashFunctions
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
# check if the user is in a fullscreen terminal, tty1 though 4 will be opened as byobu instances
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
	# set byobu backend to screen for the customized configuration to work
	byobu-select-backend screen;
	# launch byobu
	byobu;
	# exit when all terminals are closed
	exit;
fi
