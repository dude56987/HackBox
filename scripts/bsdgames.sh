#! /bin/bash
########################################################################
# Add a command to list all of the bsdgames commands
# Copyright (C) 2015  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#####################################################################
# Games & Emulation 
####################################################################
# install useability command for listing all bsd games
echo 'Installing Bsd Games (usability commands)...'
echo '#! /bin/bash
echo "Use the below commands to access the individual games"
echo "-----------------------------------------------------"
echo "ninvaders - a ascii clone of Invaders"
echo "adventure - an exploration game"
echo "arithmetic - quiz on simple arithmetic"
echo "atc - air traffic controller game"
echo "backgammon - the game of backgammon"
echo "banner - print large banner on printer"
echo "battlestar - a tropical adventure game"
echo "bcd - reformat input as punch cards, paper tape or morse code"
echo "boggle - word search game"
echo "caesar - decrypt caesar cyphers"
echo "canfield - the solitaire card game canfield"
echo "cfscores - show scores for canfield"
echo "cribbage - the card game cribbage"
echo "fish - play Go Fish"
echo "gomoku - game of 5 in a row"
echo "hangman - Computer version of the game hangman"
echo "hunt - a multi-player multi-terminal game"
echo "huntd - hunt daemon, back-end for hunt game"
echo "mille - play Mille Bornes"
echo "monop - Monopoly game"
echo "morse - reformat input as punch cards, paper tape or morse code"
echo "number - convert Arabic numerals to English"
echo "phantasia - an interterminal fantasy game"
echo "pom - display the phase of the moon"
echo "ppt - reformat input as punch cards, paper tape or morse code"
echo "primes - generate primes"
echo "quiz - random knowledge tests"
echo "rain - animated raindrops display"
echo "random - random lines from a file or random numbers"
echo "robots - fight off villainous robots"
echo "rot13 - rot13 encrypt/decrypt"
echo "sail - multi-user wooden ships and iron men"
echo "snake - display chase game"
echo "teachgammon - learn to play backgammon"
echo "tetris-bsd - the game of tetris"
echo "trek - trekkie game"
echo "wargames - shall we play a game?"
echo "worm - Play the growing worm game"
echo "worms - animate worms on a display terminal"
echo "wtf - translates acronyms for you"
echo "wump - hunt the wumpus in an underground cave "' > /usr/bin/bsdgames
# execute rights to bsdgames
sudo chmod +x /usr/bin/bsdgames
# install secondary command to list bsdgames using a system link
link /usr/bin/bsdgames /usr/bin/bsd-games
