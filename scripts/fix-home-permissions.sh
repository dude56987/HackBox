# make home directories only readable by thier owners
sudo chmod 0750 /home/*
# make the above the default for new users
sudo sed -i "s/DIR_MODE=[0987654321]\{1,4\}/DIR_MODE=0750/g" /etc/adduser.conf
