HackBox
=======

HackBox is a set of scripts designed to setup a desktop distro from a freshly installed Ubuntu based distro. It is recommended that you use it with a fresh install of Linux Mint XFCE editon, the standard Ubuntu desktop, or Xubuntu. Each of these platforms have been tested for compatiblity with the script. However this script should work on any Ubuntu based system.
###One-liner UNSTABLE Version Install
Copy and paste the below command into a terminal and hit enter to install the unstable version of HackBox.

    sudo apt-get install git python && git clone https://github.com/dude56987/HackBox.git && cd HackBox && make batman

###TO INSTALL THE PROGRAM USE THE FOLLOWING STEPS.

Open a terminal in the same folder as this README.md. Then enter the command below.

    make
 
To remove the installer installed with this method use the local package manager. For Linux Mint and Ubuntu it would be

    apt-get purge hackbox

This will install and run the program though the script that installs all the extra packages for your system. The program is seprated into sections so you can decide which tools you need on your system.

###TO RUN THE PROGRAM WITHOUT INSTALLING USE THE FOLLOWING STEPS.

1. Open a terminal in the same folder as this README.md
2. Type 'make run'
3. Hit enter

NOTE:
    It is better to use the first method mentioned. It is by far
    more tested and stable. You may uninstall the package after
    you have ran the program and the changes will persist.

To remove the software installed with the above second method.

1. Open a terminal in the same folder as this README.txt.
2. Type 'sudo make uninstallfromsystem'
3. Hit enter

NOTE:
    Nothing has been built yet to remove all the changes the program does
    to the system. Currently you would need to do a fresh reinstall of the
    operating system to clean all the changes. However the above commands
    do remove the installer itself and media assets installed.
