"This is a example vim config file with some basic stuff set."
"############################################################"
"Wrap text insted of being on one line"
set lbr
"Turn on smart indenting in line wrap mode"
if has('breakindent')
	set breakindent
endif
"Turn on line numbering"
set nu
"Set syntax Highlighting on"
syntax on
"Indent automaticly"
filetype indent on
set autoindent
"Case insensitive search"
set ic
"Highlight search"
set hls
"Turn on mouse support"
set mouse=a
