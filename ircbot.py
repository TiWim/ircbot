# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf


from lib import irclib
from lib import ircbot
import time
import requests
import re
from modules import Parler as Mod

admin = ["TiWim", "Tiwim"]
serveur = "irc.root-me.org"
canal = "#Bots_room"
robNick = "miyBtBot"
port = 6667
helloMsg = "Hi!"  # va sur Bots_room :) et réponds au bot si tu recois le message"
log_fileName = "bot.log"
log_file = open(log_fileName, "w")


class Bot(ircbot.SingleServerIRCBot):


    def on_welcome(self, serv, ev):
        serv.join(canal)
        logs("Joined channel '" + canal + "' with nickname '" + robNick + "'")
        # time.sleep(1)
        serv.privmsg(canal, helloMsg)

    def on_privmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0]
        print(auteur + " >> " + message)

        if auteur in admin:
            serv.privmsg(canal, message)
            logs("Message '" + message + "' transfered to '" + canal + "'")

            #if "stop" in message:
            #    self.on_close(serv, canal, auteur)
        else:
            public(serv, ev)
#            serv.privmsg(auteur, "bonjour, merci de m'envoyer des messages privés")
            logs("Message '" + message + "' received and answered to '" + auteur + "'")

    def on_pubmsg(self, serv, ev):
        self.public(serv, ev)

    def on_close(self, serv, canal, auteur):
        serv.privmsg(canal, "ok je me casse alors!")
        logs("Received disconnection msg from: '" + auteur + "'")
        log_file.close()
        serv.disconnect()
        self.die()

    def public(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]

        if "!apero" in message:
            logs("Requested Apero from: '" + auteur)
            try:
                serv.privmsg(canal, Mod.apero())
            except:
                print "erreur inconnue"
        elif "!weekend" in message:
            logs("Requested Weekend from: '" + auteur)
            serv.privmsg(canal, Mod.weekend())
        elif "!help" in message:
            logs("Requested Help from: '" + auteur)
            serv.privmsg(canal, "!help !reload !apero !weekend")

        elif robNick in message:
            if "stop" in message:
                logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
                self.on_close(serv, canal, auteur)
            elif "bonjour" in message:
                logs("Received Bonjour from: '" + auteur)
                serv.privmsg(canal, "bonjour " + auteur )
            elif "!reload" in message and auteur in admin:
                logs("Requested reload")
                serv.privmsg(canal, "rechargement de mes facultés")
            else:
                logs("Received '" + message + "' from: '" + auteur)
                serv.privmsg(canal, "je n'ai pas compris!")
        else:
            logs("Catched '" + message + "' from: '" + auteur)

def logs(message):
    print time.strftime("%m-%d %H:%M:%S"), "=>", message
    log_file.write(time.strftime("%m-%d %H:%M:%S") + " "
            + message + "\n")


if __name__ == "__main__":
    try:
        logs("Connecting to server '" + serveur + "'")
        Bot([(serveur, port)],robNick,robNick).start()
    except KeyboardInterrupt:
        print "\ruser interruption"
        print "closing log file and shutting down"
        log_file.close()
