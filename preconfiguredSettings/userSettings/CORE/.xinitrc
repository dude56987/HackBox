# if lxsession should only exist on low ram systems, so launch it first
if [ -f /usr/bin/lxsession ];then
	lxsession;
elif [ -f /usr/bin/xfce4-session ];then
	# xfce is the main focus desktop of hackbox so it should generally launch
	xfce4-session;
elif [ -f /usr/bin/xterm ];then
	# if all else fails launch a fullscreen xterm session so user is not stuck in a blank screen
	xterm -fullscreen
fi
