# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf

# TODO move logs to modules

from lib import ircbot
from modules import Interact
from src.confutils import readConf
from src.logutils import logs


admin = readConf("irc", "admin")
helloMsg = readConf("irc", "welcome_msg")
robNick = readConf("irc", "botnick")

def getAuthor(source):
    print(source)
    return source.split('!')[0]


class Bot(ircbot.SingleServerIRCBot):
    channel = "#" + readConf("irc", "channel")

    def on_welcome(self, serv, ev):
        print "welcome"
        serv.join(self.channel)
        logs("Joined channel " + self.channel, robNick)
        serv.privmsg(self.channel, helloMsg)

    def on_kick(self, serv, ev):
        channel = ev.target()
        author = getAuthor(ev.source())
        serv.join(self.channel)
        serv.privmsg(channel, "Méchant {}!".format(author))

    def on_privmsg(self, serv, ev):
        author = getAuthor(ev.source())
        message = ev.arguments()[0]
        print(author + " >> " + message)

        serv.join("#business")
        if author in admin:
            serv.privmsg(self.channel, message)
            logs("Message '" + message + "' transfered to '" + self.channel + "'")

        elif author == "BotInfo" or author == "BotRSS" :
            serv.privmsg(self.channel, message)
        else:
            serv.privmsg(author, "bonjour, merci de m'envoyer des messages privés")
            logs("Message '" + message + "' received and answered", author, "\33[01;31mmsg\33[0m")

    def on_pubmsg(self, serv, ev):
        author = getAuthor(ev.source())
        channel = ev.target()
        message = ev.arguments()[0]
        print message
        if "!reload" in message and author in admin:
            reload(Interact)
            serv.privmsg(channel, "I g0t m0r3 P0w4!")
        else:
            Interact.public(self, serv, author, channel, message)

    def on_close(self, serv, author):
        #serv.privmsg(self.channel, "ok je me casse alors!")
        #logs("Received disconnection msg from: '" + author + "'")
        self.die()

