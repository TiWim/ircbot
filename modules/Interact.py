#! /usr/env/python
# coding: utf-8

from Parler import apero, weekend
import Parler as Mod
from src.logutils import logs
from src.confutils import readConf

admin = readConf('irc', 'admin')
robNick = readConf('irc', 'botnick')

def load():
    reload(Mod)

def cafe():
    return "dis donc, tu me prends pour un esclave?"

def biere():
   return "Et un openbar, un!"

def pastis(serv, auteur, canal, message):
    serv.kick(canal, auteur, "tu me prends pour un serveur?")

def public(client, serv, auteur, canal, message):
    parse = message.split(' ')

    commandes = { 
            "!apéro" : apero,
            "!weekend" : weekend,
            "!café" : cafe,
            "!bière" : biere,
            "!pastis" : pastis,
            }
    if message == "!help":
        string = ""
        for key in commandes:
            string += key + " "
        serv.privmsg(canal, string.strip())
        return
    else:
        try:
            retValue = commandes[message]()
            serv.privmsg(canal, retValue)
        except TypeError:
            commandes[message](serv, auteur, canal, message)
        except Exception as e:
            print e
            print("failed")



    if message == "!ctfs":
        liste = Mod.ctf()
        for elt in liste:
            serv.privmsg(canal, elt)
    elif "!nick" in message:
        msg = message.split(" ")
        if len(msg) >= 2:
            serv.nick(msg[1])
        else:
            serv.privmsg(canal, "il faut un nom!")
    elif "!ctf" == message.split(" ")[0]:
        logs("Requested ctf score")
        try:
            serv.privmsg(canal, Mod.score(message.split(" ")[1]))
        except:
            serv.privmsg(canal, Mod.score())
    elif message == "!op":
        serv.mode(canal, "+o TiWim")
    elif robNick in message:
        if "stop" in message:
            if auteur in admin:
                logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
                client.die("A bientôt")
            else:
                serv.privmsg(canal, "Méchant " + auteur + " tu voulais me faire partir?")
                logs("sent stop signal!", auteur, "\33[01;31mWARN\33[0m")
        elif "bonjour" in message:
            logs("Received Bonjour from: '" + auteur)
            serv.privmsg(canal, "bonjour " + auteur)
        else:
            logs("Received '" + message + "' from: '" + auteur)
    else:
        parse = message.strip().split(' ')
        if parse[0] in ['!score','!s','!last','!lastflag', '!chall', '!challenges']:
            if len(parse) >= 2:
                serv.privmsg("BotRSS", message)
                serv.privmsg("BotInfo", message)
            else:
                serv.privmsg("BotInfo", parse[0] + " " + auteur)
        elif "!choosechall" == parse[0]:
            nick = auteur
            if len(parse) >= 2:
                nick = parse[1]
            serv.privmsg(canal, Mod.choosechall(nick))
        elif len(parse) == 3 and parse[0] == "kick" and parse[2] == "please":
            serv.privmsg(canal, "Yes Master!")
            if parse[1] in admin:
                serv.kick(canal, auteur, "Héhé, DTC")
            else:
                serv.kick(canal, parse[1], "haha")
