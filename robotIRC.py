# -*- coding: utf-8 -*-
# http://openclassrooms.com/courses/programmer-un-bot-irc-simplement-avec-ircbot
# http://www.devshed.com/c/a/Python/IRC-on-a-Higher-Level-Concluded/
# https://user.oc-static.com/pdf/102516-programmer-un-bot-irc-simplement-avec-ircbot.pdf


from lib import irclib
from lib import ircbot
import time
import requests
import re
from modules import Parler

admin = ["TiWim", "Tiwim"]
serveur = "irc.root-me.org"
canal = "#Bots_room"
robNick = "myBot"
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

            if "stop" in message:
                self.on_close(serv, canal, auteur)
        else:
            serv.privmsg(auteur, "bonjour, merci de m'envoyer des messages privés")
            logs("Message '" + message + "' received and answered to '" + auteur + "'")

    def on_pubmsg(self, serv, ev):
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0]

        if robNick in message:
            logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
            if "stop" in message:
                self.on_close(serv, canal, auteur)
            elif "apero" in message:
                logs("Received apero order from: '" + auteur)
                message = apero()
                serv.privmsg(canal, message)
            elif "bonjour" in message:
                logs("Received Bonjour from: '" + auteur)
                serv.privmsg(canal, "bonjour " + auteur )
            elif "!reload" in message and auteur == "TiWim":
                serv.privmsg(canal, "rechargement de mes facultés")
            else:
                logs("Received '" + message + "' from: '" + auteur)
                serv.privmsg(canal, "je n'ai pas compris!")
        elif "!help" in message:
            serv.privmsg(canal, "!help !reload apero")


        #self.public(auteur, canal, message)

    def on_close(self, serv, canal, auteur):
        serv.privmsg(canal, "ok je me casse alors!")
        logs("Received disconnection msg from: '" + auteur + "'")
        log_file.close()
        serv.disconnect()
        self.die()

    def public(self, auteur, canal, message):
        if "!apero" in message:
            logs("Requested Apero from: '" + auteur)
            serv.privmsg(canal, apero())
        elif "!weekend" in message:
            logs("Requested Weekend from: '" + auteur)
            serv.privmsg(canal, weekend())
        elif "!help" in message:
            logs("Requested Help from: '" + auteur)
            serv.privmsg(canal, "!help !reload !apero !weekend")

        elif robNick in message:
            if "stop" in message:
                logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
                self.on_close()
            elif "bonjour" in message:
                logs("Received Bonjour from: '" + auteur)
                serv.privmsg(canal, "bonjour " + auteur )
            elif "!reload" in message and auteur in admin:
                logs("Requested reload")
                serv.privmsg(canal, "rechargement de mes facultés")
            else:
                logs("Received '" + message + "' from: '" + auteur)
                serv.privmsg(canal, "je n'ai pas compris!")


def logs(message):
    print time.strftime("%m-%d %H:%M:%S"), "=>", message
    log_file.write(time.strftime("%m-%d %H:%M:%S") + " "
            + message + "\n")

def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = requests.get(page).text
    return re.search('<font size=5>(.*)</font>', resultat).group(1)

def weekend():
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()


if __name__ == "__main__":
    try:
        logs("Connecting to server '" + serveur + "'")
        Bot([(serveur, port)],robNick,robNick).start()
        #bot().start()
        logs("Connected")
    except KeyboardInterrupt:
        print "user interruption"
        print "closing log file and shutting down"
        log_file.close()


