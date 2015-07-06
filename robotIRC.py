# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
import irclib
import ircbot
import time
import sys
from modules import Parler

serveur = "irc.root-me.org"
canal = "#root-me_bots"
robNick = "jeannot2"
helloMsg = "hi!"
log_fileName = "bot.log"
log_file = open(log_fileName, "w")

def logs(message):
    print time.strftime("%m-%d %H:%M:%S"), "=>", message
    log_file.write(time.strftime("%m-%d %H:%M:%S") + " "
            + message + "\n")

class Bot(ircbot.SingleServerIRCBot):

    def __init__(self):
        logs("Connecting to server '" + serveur + "'")
        ircbot.SingleServerIRCBot.__init__(self, [(serveur, 6667)],robNick,robNick)
        logs("Connected")

    def on_welcome(self, serv, ev):
        serv.join(canal)
        logs("Joined channel '" + canal + "' with nickname '" + robNick + "'")
#        time.sleep(1)
        serv.privmsg(canal, helloMsg)

    def on_privmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        print(auteur + " >> " + message)

        if auteur == "TiWim":
            serv.privmsg(canal, message)
            logs("Message '" + message + "' transfered to '" + canal + "'")

            if "stop" in message:
                self.on_close()


    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]

        if robNick in message:
            logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
            if "stop" in message:
                self.on_close()

            elif "apero" in message:
                logs("Received apero order from: '" + auteur)
                serv.privmsg(canal, "pas encore implémenté :(")
            elif "bonjour" in message:
                logs("Received Bonjour from: '" + auteur)
                serv.privmsg(canal, "bonjour " + auteur )
            elif "!reload" in message and "TiWim":
                serv.privmsg(canal, "rechargement de mes facultés")
            else:
                logs("Received '" + message + "' from: '" + auteur)
                serv.privmsg(canal, "je n'ai pas compris!")
        elif "!help" in message:
            serv.privmsg(canal, "!help !reload apero")


        #self.public(auteur, canal, message)

    def on_close(self):
        serv.privmsg(canal, "ok je me casse alors!")
        logs("Received disconnection msg from: '" + auteur)
        log_file.close()
        serv.disconnect()
        sys.exit()

    def public(self, auteur, canal, message):
        if robNick in message:
            logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
            if "stop" in message:
                self.on_close()

            elif "apero" in message:
                logs("Received apero order from: '" + auteur)
                serv.privmsg(canal, "pas encore implémenté :(")
            elif "bonjour" in message:
                logs("Received Bonjour from: '" + auteur)
                serv.privmsg(canal, "bonjour " + auteur )
            elif "!reload" in message and "TiWim":
                serv.privmsg(canal, "rechargement de mes facultés")
            else:
                logs("Received '" + message + "' from: '" + auteur)
                serv.privmsg(canal, "je n'ai pas compris!")
        elif "!help" in message:
            serv.privmsg(canal, "!help !reload apero")

if __name__ == "__main__":
    try:
        Bot().start()
    except KeyboardInterrupt:
        print "user interruption"
