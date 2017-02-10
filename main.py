# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf

import time
from src.confutils import readConf
from src.logutils import logs
from src.ircbot import Bot

admin = readConf("irc", "admin")
serveur = readConf("irc", "server")
canal = readConf("irc", "channel")
robNick = readConf("irc", "botnick")
port = readConf("irc", "port")
helloMsg = readConf("irc", "welcome_msg")

if __name__ == "__main__":

    bot = (Bot)

    try:
        logs("Connecting to server '" + serveur + port + robNick + "'")
        bot = Bot([(serveur, 6667)], robNick, robNick)
        bot.start()
    except KeyboardInterrupt:
        print "\ruser interuption"
#        bot.on_close() 
        print "closing log file and shutting down"
