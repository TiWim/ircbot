#! /usr/env/python
# coding: utf-8

import Parler as Mod
from src.logutils import logs
from src.confutils import readConf

admin = readConf('irc', 'admin')
robNick = readConf('irc', 'botnick')

def public(client, serv, auteur, canal, message):
    parse = message.split(' ')

    if "!apero" in message:
        logs("Requested Apero", auteur)
        try:
            serv.privmsg(canal, Mod.apero())
            logs("Command answered")
        except:
            serv.privmsg(canal, "Parsing error http://estcequecestbientotlapero.fr")
            logs("Command unsuccessful", author=auteur, info="WARN")
    elif "!weekend" in message:
        try:
            logs("requested Weekend", auteur)
            serv.privmsg(canal, Mod.weekend())
        except:
            logs("Failure!", info="Debug")
            serv.privmsg(canal, "marche pas :(")
    elif message == "!ctfs":
        liste = Mod.ctf()
        for elt in liste:
            serv.privmsg(canal, elt)
    elif "!help" == message:
        logs("Requested Help from: '" + auteur)
        serv.privmsg(canal, "!help !ctf !ctfs !reload !apero !weekend !pastis")
    elif message in "!pastis":
        serv.kick(canal, auteur, "tu me prends pour un serveur?")
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
    elif message == "!café":
        serv.privmsg(canal, "dis donc, tu me prends pour un esclave?")
    elif message == "!biere":
        serv.privmsg(canal, "Et un openbar, un!")
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
        print parse
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
