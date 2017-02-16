# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf

import time
from src.confutils import readConf
from src.logutils import logs
from src.ircclient import Bot

admin = readConf("irc", "admin")
server = readConf("irc", "server")
canal = readConf("irc", "channel")
robNick = readConf("irc", "botnick")
port = int(readConf("irc", "port"))
helloMsg = readConf("irc", "welcome_msg")
password = readConf("irc", "password")
ssl = readConf("irc", "ssl")

# Bot( [tuple of servers], nick, real_name)
# tuple of servers = (server, port, password=None, ssl=False)
if __name__ == "__main__":

    bot = (Bot)

    try:
        logs("Connecting to server '" + server + "'")
        bot = Bot([(server, port, password, ssl)], robNick, robNick)
        bot.start()
    except KeyboardInterrupt:
        print "\ruser interuption, closing bot"
        bot.die("Coming back soon") 
