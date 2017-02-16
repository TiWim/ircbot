#! /usr/env/python
# coding: utf-8

from Parler import *
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

def op(serv, auteur, canal, message):
    serv.mode(canal, "+o TiWim")

def renick(serv, auteur, canal, message):
    msg = message.split(" ")
    if len(msg) >= 2:
        serv.nick(msg[1])
    else:
        serv.privmsg(canal, "il faut un nom!")

def part(client, serv, auteur, canal, message):
    if auteur in admin:
        logs("Received message '" + message + "' from '" + auteur + "' on '" + canal + "'")
        client.die("A bientôt")
    else:
        serv.privmsg(canal, "Méchant " + auteur + " tu voulais me faire partir?")
        logs("sent stop signal!", auteur, "\33[01;31mWARN\33[0m")


def public(client, serv, auteur, canal, message):
    parse = message.split(' ')

    commandes = { 
            "!apéro" : apero,
            "!weekend" : weekend,
            "!café" : cafe,
            "!bière" : biere,
            "!rosé" : pastis,
            "!op" : op,
            "!reload" : None,
            "!bye" : part,
            }
    commandes_arg = {
            "!choosechall" : choosechall, #(auteur, message),
            "!nick" : renick, # (serv, canal, message),
            }

    if message == "!help":
        string = ""
        for key in commandes:
            string += key + " "
        for key in commandes_arg:
            string += key + "<arg> "
        serv.privmsg(canal, string.strip())
        return
    elif message == "!bye":
        part(client,serv, auteur, canal, message)
    else:
        try:
            retValue = commandes[message]()
            #if retValue:
            serv.privmsg(canal, retValue)
        except TypeError as e:
            print e
            """ Commandes ayant besoin de parametres """
            commandes[message](serv, auteur, canal, message)
        except KeyError as e:
            print e
            try:
                ret = commandes_arg[parse[0]](serv,auteur,canal, message)
                if ret:
                    serv.privmsg(canal, ret)
            except Exception as e:
                print e
        except Exception as e:
            print e
            print("failed")



   # if message == "!ctfs":
   #     liste = Mod.ctf()
   #     for elt in liste:
   #         serv.privmsg(canal, elt)
   # elif robNick in message:
   #     if "bonjour" in message:
   #         logs("Received Bonjour from: '" + auteur)
   #         serv.privmsg(canal, "bonjour " + auteur)
   #     else:
   #         logs("Received '" + message + "' from: '" + auteur)
   # else:
   #     parse = message.strip().split(' ')
   #     if parse[0] in ['!score','!s','!last','!lastflag', '!chall', '!challenges']:
   #         if len(parse) >= 2:
   #             serv.privmsg("BotRSS", message)
   #             serv.privmsg("BotInfo", message)
   #         else:
   #             serv.privmsg("BotInfo", parse[0] + " " + auteur)
   #     elif len(parse) == 3 and parse[0] == "kick" and parse[2] == "please":
   #         serv.privmsg(canal, "Yes Master!")
   #         if parse[1] in admin:
   #             serv.kick(canal, auteur, "Héhé, DTC")
   #         else:
   #             serv.kick(canal, parse[1], "haha")
