HackBox
=======

HackBox is a set of scripts designed to setup a desktop distro from a freshly installed Ubuntu based system.

This package is designed with a few key points in mind.
- Defaults Should be Sane and Secure.
- User customization should be as in depth as the user wants to go.
- You should be able to work without the Internet.
- The system should attempt to support decentralization technologies as much as possible.

### One-liner UNSTABLE Version Install
Copy and paste the below command into a terminal and hit enter to install the unstable version of HackBox.

    sudo apt-get install git python gdebi make && git clone https://github.com/dude56987/HackBox.git && cd HackBox && make && hackboxsetup

### INSTALL

#### Dependencies
You may need to install make and git in order to pull and build the software. You can install them on ubuntu with the below command.

	sudo apt-get install make git gdebi --assume-yes

Once you have installed these all other dependency checking is handled automatically.

#### Downloading
You can download the source to build the installer with the below command.

	git clone https://github.com/dude56987/hackbox

#### Building Source
Once you have this repository downloaded. Open a terminal in the same folder as this README.md. Then enter the command below.

    make

### USAGE
You can launch the program from the command line with the following command.

    hackboxlauncher

Or you can launch the graphical version with the command.

    hackboxsetup-gui

### UPGRADE
You can run "HackBox Upgrade" from the start menu. This will download the newest version of HackBox and install it. After HackBox has been upgraded it will run hackboxsetup-gui to update the system configuration. You can also launch a upgrade from the command line with the below command.

    hackboxsetup --upgrade

Be sure to backup any configuration you wish to perserve.

### UNINSTALL
To remove the installer installed with this method use the local package manager. For Linux Mint and Ubuntu it would be

    sudo apt-get purge hackbox

#### NOTE:

	Currently you would need to do a fresh reinstall of the operating system to clean all the changes. However the above commands do remove the installer itself and most media assets installed.
