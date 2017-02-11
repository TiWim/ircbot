#! /usr/env/python
# coding: utf-8

from sys import stdout
from traceback import print_exc
from subprocess import Popen, PIPE
import re
from random import randint

def get(page):
    value = Popen("curl {}".format(page), stdout=PIPE, shell=True).communicate()[0]
    try:
        value = value.encode("utf-8")
    except:
        pass
    return value

try:
    from bs4 import BeautifulSoup
except:
    print 'Vous devez installer le paquet python-bs4'

def apero():
    """
    take the content of the website and print it on the chan
    """
    page = "http://estcequecestbientotlapero.fr"
    resultat = BeautifulSoup(get(page), "lxml")
    return resultat.h2.text.encode('utf-8').replace(".", ". ").strip()

def choosechall(nick):
    if nick == "ghozt":
        nick = "Ghozt-30087"
    p = re.compile(ur'class="rouge".*?href="(.*?)".*?"(.*?)".*?;(.*?)<')

    page = "http://www.root-me.org/" + nick + "?inc=score&lang=fr"
    resultat = get(page)
    result = ""
    try:
        liste = re.findall(p, resultat)
        size = len(liste)
        if size != 0:
            random = randint(0, size - 1)
            print random
            result = liste[random][2] + " (" + liste[random][1] + ") Lien: http://www.root-me.org/" + liste[random][0]
        else:
            result = "No more challenges availables"
    except:
        result = "This challenger doesn't exist"
    return result


def weekend():
    """
    take the content of the website and print it on the chan
    """
    page = "http://estcequecestbientotleweekend.fr"
    resultat = get(page)
    res = re.search(ur'<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    return res.replace("&#039;","'")


def score(team='Tontons'):
    """
    This class has to be changed before each new ctf.
    get param: page and verify=False for corrupted ssl certs
    """
    try:
        page = "https://school.fluxfingers.net/scoreboard"
        p = re.compile(ur'number">(.*?)<.*>(.*?)<\/a.*number">(.*?)<\/td><\/tr>')
        resultat = get(page).replace("\n", "").replace(" ", "").split("<tr")
        for i in resultat:
            if team.lower() in i.lower():
                a = re.search(p, i)
                b = int(a.group(1))
                string = "Classement: " + a.group(2) + " " + str(b)
                if b == 1:
                    string += "ers avec "
                else:
                    string += "èmes avec "

                return string + a.group(3) + " points!"
    except:
        print_exc(file=stdout)
        return "failure"


def ctf():
    """
    returns a list of ctfs
    """
    try:
        page = "https://ctftime.org/event/list/upcoming/rss/"
        p = re.compile(ur'<item><title>(.*?)<.*?Date(.*?)\&.*?sh;(.*?) &.*?at: (.*?)&lt.*?b&gt;(.*?)&.*?href="(.*?)"')
        test_str = get(page).strip().replace("\n", "")
        liste = re.findall(p, test_str)
        compteur = 0
        string = []
        while liste:
            elt = liste.pop(0)
            if "On-site" in elt[4]:
                continue
            compteur += 1
            line = "\x0304" + elt[0] + "\x03 Dates\x0302" + elt[1]
            line += "-" + elt[2] + "\x03 type: \x0302" + elt[3]
            line += "\x03 Site web: \x0303" + elt[5] + "\x03"
            string.append(line)
            if compteur == 5:
                break
        return string
    except:
        print_exc(file=stdout)
        return "failure"

