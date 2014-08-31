#! /bin/bash
# add message of the day script to system startup
sed -i "s/exit 0//g" /etc/rc.local
sed -i "s/message-of-the-day//g" /etc/rc.local
echo 'message-of-the-day' >> /etc/rc.local
echo 'exit 0' >> /etc/rc.local
# clear blank lines from the file
sed -i '/^$/d' /etc/rc.local
# write the message of the day script
echo "#! /bin/bash" > /usr/bin/message-of-the-day
echo 'for dir in /home/*;do' >> /usr/bin/message-of-the-day
echo "echo \"Editing \$dir/.motd ...\"" >> /usr/bin/message-of-the-day
echo "fortune -a > \$dir/.motd" >> /usr/bin/message-of-the-day
echo "chown \$(echo \$dir | sed \"s/\/home\///g\") \$dir/.motd" >> /usr/bin/message-of-the-day
echo 'done' >> /usr/bin/message-of-the-day
chown root /usr/bin/message-of-the-day
chmod u+xr /usr/bin/message-of-the-day
chmod go-wx /usr/bin/message-of-the-day
chmod go+r /usr/bin/message-of-the-day
