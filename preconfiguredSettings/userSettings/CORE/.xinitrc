if [ -f /usr/bin/xfce4-session ];then
	xfce4-session;
elif [ -f /usr/bin/lxsession ];then
	lxsession;
fi
