"############################################################"
"This is a example vim config file with some basic stuff set."
"############################################################"
" Create alias for spell-checker, use :Spellcheck to turn it on"
command Spellcheck setlocal spell spelllang=en_us
"Commands to convert between tabs and spaces"
command TabsToSpaces set et | ret!
command SpacesToTabs set et! | ret!
"Command to make whitespace visible"
command ShowWhitespace set list
command HideWhitespace set list!
"Strip trailing whitespace from all lines in a file"
command StripTrailingWhitespace :%s/\s\+$//e
"Auto strip trailing whitespace when saving files"
autocmd BufWritePre * :%s/\s\+$//e
"Wrap text instead of being on one line"
set lbr
"Turn on smart indenting in line wrap mode"
if has('breakindent')
	set breakindent
endif
"Turn on line numbering"
set number
"Set syntax Highlighting on"
syntax on
"Indent automatically"
filetype indent on
set autoindent
"Case insensitive search"
set ic
"Highlight search"
set hls
"Highlight the current line"
set cul
"Turn on mouse support"
set mouse=a
"Change the default color scheme"
"The following are the color schemes available by default"
"blue darkblue default delek desert elflord evening koehler morning murphy pablo peachpuff ron shine slate torte zellner"
colorscheme ron
"Set tab width to 4 and shift width to 4 to line up with tabs"
set tabstop=4
set shiftwidth=4
