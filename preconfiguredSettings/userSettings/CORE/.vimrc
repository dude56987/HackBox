"############################################################"
"This is a example vim config file with some basic stuff set."
"############################################################"
" Create alias for spell-checker, use :Spellcheck to turn it on"
command Spellcheck setlocal spell spelllang=en_us
"Wrap text instead of being on one line"
set lbr
"Turn on smart indenting in line wrap mode"
if has('breakindent')
	set breakindent
endif
"Turn on line numbering"
set nu
"Set syntax Highlighting on"
syntax on
"Indent automatically"
filetype indent on
set autoindent
"Case insensitive search"
set ic
"Highlight search"
set hls
"Turn on mouse support"
set mouse=a
"Change the default color scheme"
colorscheme ron
"The following are the color schemes available by default"
"blue darkblue default delek desert elflord evening koehler morning murphy pablo peachpuff ron shine slate torte zellner"
