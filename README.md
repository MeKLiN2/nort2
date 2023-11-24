zxc@qwe:~/nort2$ python2 nortbot.py
INFO:__main__:Starting Nortbot v 1.1.0.7
Login? [type yes or press enter=no] raise
DEBUG:util.worker:threaded task, target=<bound method NortBot.connect of <bot.NortBot instance at 0x7efcdd5b2f50>>, args=()
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): tinychat.com:443
DEBUG:urllib3.connectionpool:https://tinychat.com:443 "GET /api/v1.0/room/token/cancers HTTP/1.1" 500 None
[13:23:37:540] Error during request: HTTP error. Status code: None
[13:23:37:540] Exception details: HTTP error. Status code: None
INFO:tinychat:missing connect args None

----------------------------------------

2023-11-23 20:30:18,252 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:30:19,615 : INFO : tinychat.py : 274 : connect() : tinychat : missing connect args None
2023-11-23 20:30:22,463 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:30:23,584 : INFO : tinychat.py : 274 : connect() : tinychat : missing connect args None
2023-11-23 20:32:00,176 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:39:45,763 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:40:39,557 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:47:36,883 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:48:12,969 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 20:49:27,257 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:00:21,968 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:01:04,498 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:02:29,115 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:06:50,280 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:08:49,284 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:16:18,157 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:19:37,426 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:36:42,860 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7
2023-11-23 21:41:18,889 : INFO : nortbot.py : 105 : <module>() : __main__ : Starting Nortbot v 1.1.0.7

----------------------------------------

## Nortbot

A bot for Tinychat chat rooms.

This started out with some improvements to a few files for the bot in the room I go to. This basically led to a complete rewrite of almost everything.


## Setup
For a Windows user that wants a bot without having to deal with the Python aspect, I have provided a compiled Windows executable in the [**Releases**](https://github.com/nortxort/nortbot/releases) section.

It is somewhat based on pinylib-rtc/tinybot-rtc so Python 2.7.16+ is required. It has been tested on Windows 10, Debian 9/10, and Ubuntu 16/18/19.


### Requirements

[Requirements.txt](https://github.com/nortxort/nortbot/blob/master/requirements.txt) contains a list of requirements which can be installed with `pip install -r /path/to/requirements.txt`


## Usage

Change [config.ini](https://github.com/nortxort/nortbot/blob/master/config.ini) settings to fit your needs. ***Don’t forget to change the default key!*** Then run `nortbot.py`. 

For a detailed explanation of the different config settings, read through the [**config settings**](https://github.com/nortxort/nortbot/blob/master/CONFIG.md).

Command explanations can be found [**HERE**](https://github.com/nortxort/nortbot/blob/master/COMMANDS.md).


## Compiling

In order to compile simply run `compile.bat`, located in the `compile` folder. You will need the following:
* Python 2.7.16+ in your path.
* Possibly [Microsoft Visual C++ 2008 Redistributable Package](http://www.microsoft.com/downloads/en/details.aspx?FamilyID=9b2da534-3e03-4391-8a4d-074b9f2bc1bf&displaylang=en).
* May need elevated permission on first run.

*More details about pyinstaller's requirements can be found [HERE](https://pyinstaller.readthedocs.io/en/v3.3.1/usage.html#windows)*


### Using Pyinstaller

You will need [pyinstaller](http://www.pyinstaller.org/), it can be installed with the following command: `pip install pyinstaller` 

Next, change directory to the directory containing the source code: `cd path/to/source/code/files` 

from there run: `pyinstaller --onefile nortbot.py`.

2 new directories will be created, build and dist. The **dist** directory will contain **nortbot.exe**. Copy **cacert.pem** and **config.ini** to the **dist** directory.

You can now run `nortbot.exe`!


## Submitting an issue

Please read through the [ISSUES](https://github.com/nortxort/nortbot/issues) before submitting a new one. If you want to submit a new issue, then use an [ISSUE TEMPLATE](https://github.com/nortxort/nortbot/issues/new/choose). **_Please_ use an issue template, they're there for a reason!** If you need more help or have questions that are not already answered in the issues, you can [join this Discord server](https://discord.gg/cHawfkb).


## Author

* [nortxort](https://github.com/nortxort)


## License

The MIT License (MIT)
See [LICENSE](https://github.com/nortxort/nortbot/blob/master/LICENSE) for more details.


## Acknowledgments

*Thanks to the following people, who in some way or another, have contributed to this project:*

[Technetium1](https://github.com/Technetium1)

[Aida](https://github.com/Autotonic)
