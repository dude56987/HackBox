# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# Stop screen blanking issue on some systems
xset s 0 0
xset s off
xset -dpms

# rename libpurple default users with username if exists
if more ~/.purple/accounts.xml | grep AwesomeUserWhoMightBeANoob; then
	IRCusername=$(echo $(whoami)$RANDOM"@")
	username=$(echo $(whoami)"@"$(hostname))
	sed -i.bak "s/AwesomeUserWhoMightBeANoob@/${IRCusername}/g" ~/.purple/accounts.xml
	sed -i.bak "s/AwesomeUserWhoMightBeANoob/${username}/g" ~/.purple/accounts.xml
fi
