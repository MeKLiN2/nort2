# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2019 Nortxort

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import time
import logging
import bot
import re
from util import thread_task
from page import acc  # Import the acc module

log = logging.getLogger(__name__)

def is_valid_string(input_str):
    if input_str is None:
        return False

    if not isinstance(input_str, basestring):  # Use basestring for Python 2
        return False

    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, input_str))


# Add this function to handle the login logic
def handle_login(bot_client):
    if bot_client.account is None:
        bot_client.account = input('Account: ').strip()
    if bot_client.account == '/':
        main()
        return
    if bot_client.password is None:
        bot_client.password = input('Password: ')
    if bot_client.password == '/':
        main()
        return
    else:
        if bot_client.password == '//' or bot_client.password == '//':
            return False
        else:
            is_logged_in = bot_client.login()

    if not is_logged_in:
        bot_client.account = None
        bot_client.password = None
        # Use self.console.write here
        bot_client.console.write('Failed to log in. Check your credentials.', Color.B_RED)
        return False

    return True

def logger_setup():
    if bot.CONF.DEBUG_TO_FILE:
        fmt = '%(asctime)s : %(levelname)s : %(filename)s : ' \
              '%(lineno)d : %(funcName)s() : %(name)s : %(message)s'

        logging.basicConfig(filename=bot.CONF.DEBUG_FILE_NAME,
                            level=bot.CONF.DEBUG_LEVEL, format=fmt)
    else:
        log.addHandler(logging.NullHandler)

def main():
    # Create a console instance for the bot
    bot_console = acc.Console(room=bot.CONF.ROOM,
                              log_path=bot.CONF.CONFIG_PATH,
                              chat_logging=bot.CONF.CHAT_LOGGING,
                              use_colors=bot.CONF.CONSOLE_COLORS)

    # Pass the console instance to the Account class
    bot_account = acc.Account(console=bot_console)

    if bot.CONF.ROOM is None:
        bot.CONF.ROOM = input('Enter room name: ').strip()

    if bot.CONF.NICK is None:
        bot.CONF.NICK = input('Enter nickname (optional): ').strip()

    if bot.CONF.ACCOUNT is not None and bot.CONF.PASSWORD is not None:
        bot_client = bot.NortBot(bot.CONF.ROOM, nick=bot.CONF.NICK,
                                 account=bot_account,
                                 password=bot.CONF.PASSWORD)
    else:
        bot_client = bot.NortBot(bot.CONF.ROOM, nick=bot.CONF.NICK)

    # Add auto-login logic
    if bot.CONF.AUTO_LOGIN:
        do_login = True
        if bot_client.account is None or bot_client.password is None:
            log.warning("Auto-login is enabled but account/password is not provided. "
                        "Please configure account and password in the configuration.")
            do_login = False
        else:
            do_login = handle_login(bot_client)

    else:
        do_login = raw_input('Login? [type yes or press enter=no] ')
        if do_login.lower() == 'yes':
            do_login = handle_login(bot_client)
        else:
            do_login = False

    if not do_login:
        bot_client.account = None
        bot_client.password = None

    thread_task(bot_client.connect)

    while not bot_client.connected:
        time.sleep(2)

if __name__ == '__main__':
    acc.logger_setup()  # Call the logger_setup from the acc module
    log.info('Starting Nortbot v %s' % bot.CONF.BOT_VERSION)
    main()

