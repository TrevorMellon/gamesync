# GameSync
GameSync will push your save files to another folder categorized by game name. It was created primarily to sync with a nextcloud server folder.

Truth be told it doesn't have to sync just games, it could be anything.

### Requirements
* python3
* rsync
* games

## Tutorial
First step is to run the init:
* > python3 gamesync.py --init

That will ask you for which folder to sync with, eg. your nextcloud folder

To create your first sync do:
* > python3 gamesync.py -n "Name of Game"

Afterwards sync with:
* > python3 gamesync.py --verbose
or with just an overview:
* > python3 gamesync.py

## Help
You can get a liting of all options with:
* > python3 gamesync.py --help

## Installing

* > sudo cp ./gamesync.py /usr/local/bin/gamesync

## Editing

Go to ~/.config/gamesync/games-available
Edit any of the files.
Change "Game" to be the new game name.
"gamefolder" to point to the save file location.
Save and the copy the file to games-enabled
call the sync program

