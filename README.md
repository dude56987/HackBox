HackBox
=======

HackBox is a set of scripts designed to setup a desktop distro from a freshly installed Ubuntu based distro. It is recommended that you use it with a fresh install of Linux Mint XFCE edition, the standard Ubuntu desktop, or Xubuntu. Each of these platforms have been tested for compatibility with the script. However this script should work on any Ubuntu based system.

This package is designed with a few key points in mind.
- Defaults Should be Sane and Secure.
- User customization should be as in depth as the user wants to go.
- You should be able to work without the Internet.
- The system should attempt to support decentralization technologies as much as possible.

###One-liner UNSTABLE Version Install
Copy and paste the below command into a terminal and hit enter to install the unstable version of HackBox.

    sudo apt-get install git python gdebi && git clone https://github.com/dude56987/HackBox.git && cd HackBox && make install

###INSTALL

If you are on the webpage you will first have to download and unzip the repository. You can download this repo at the link below.

https://github.com/dude56987/HackBox/archive/master.zip

Once you have this repository downloaded and extracted. Open a terminal in the same folder as this README.md. Then enter the command below. 

    make install

###USAGE

You can launch the program from the command line with the following command.

    hackboxsetup
    
Or you can launch the graphical version with the command.

    hackboxsetup-gui

###UPGRADE
To upgrade the existing version use the folloing command. 

    hackboxsetup --upgrade

Be sure to backup any configuration you wish to perserve. This is a major upgrade process.

###UNINSTALL
To remove the installer installed with this method use the local package manager. For Linux Mint and Ubuntu it would be

    sudo apt-get purge hackbox

####NOTE:

    Nothing has been built yet to remove all the changes the program does
    to the system. Currently you would need to do a fresh reinstall of the
    operating system to clean all the changes. However the above commands
    do remove the installer itself and most media assets installed.
