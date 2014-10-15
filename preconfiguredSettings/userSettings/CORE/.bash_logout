# ~/.bash_logout: executed by bash(1) when login shell exits.
# empty the cache and thumbnails and the trash on logout
echo "Clearing up thumbnails..."
rm -vr ~/.thumbs &
rm -vr ~/.thumbnails &
echo "Clearing up the cache..."
rm -vr ~/.cache &
echo "Clearing recently used..."
rm -v ~/.local/share/recently-used.xbel &
echo "Emptying the trash..."
rm -vr ~/.local/share/Trash 
# when leaving the console clear the screen to increase privacy
if [ "$SHLVL" = 1 ]; then
    [ -x /usr/bin/clear_console ] && /usr/bin/clear_console -q
fi
echo "Kill all remaining user processes..."
killall -u $(echo $HOME | sed "s/\/home\///g")
