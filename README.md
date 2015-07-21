# CaveBot

Telegram bot written in python3 to play Colossal Cave Adventure. It uses a
modified version of Brandon Rhodes'
[adventure](https://pypi.python.org/pypi/adventure/1.3) library as a backend.

## Installation

### Requirements

You need to build and install the adventure library contained in the folder
`adventure-1.3` by using the following commands:
```bash
$ python3 setup.py build
$ sudo python3 setup.py install
```
Moreover the following libraries should be installed:
 * [python-telegram-bot-api](https://github.com/puehcl/python-telegram-bot-api)
 * requests
 * pexpect

### API key

Telegram's bot API requires and api key that should be placed inside a file
named 'apikey.txt'. This key can be obtained by following the instuctions on
<https://core.telegram.org/bots/api>.

## Run

To run the program simpy issue: `python3 CaveBot.py`

To exit type Ctrl+C

## How it works

This program forks an instance of Colossal Cave Adventure for each chat. It is
not very efficient but I wanted something quick and dirty that works
(contibutions and improvements are welcome). The class responsible of
communication between the main process and the forked one is called 'BLAHBLAH'

To avoid wasting resources a simple garbage collector hase been implemented.
Inactive processes are automatically stopped and their data is saved. When a
request for a stopped process arrives a new process is transparently respawned
and its data is restored. The class holding the list of processes is named
'blablu'.

## License

Copyright (C) 2015 - The Electric Ant

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses>
