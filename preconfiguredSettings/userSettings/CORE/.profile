# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# disable overlay/autohide scrollbars
export LIBOVERLAY_SCROLLBAR=0
export GTK_OVERLAY_SCROLLING=0
gdbus call --session --dest org.freedesktop.DBus --object-path /org/freedesktop/DBus --method org.freedesktop.DBus.UpdateActivationEnvironment '{"GTK_OVERLAY_SCROLLING": "0"}'

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

# Setup the current login fortune for the user
fortune -a > ~/.motd

# launch .first_start script if it exists
if [ -f ~/.first_start ]; then
	bash ~/.first_start
	rm -v ~/.first_start
fi
