#! /usr/env/python
import requests
import re
try:
    from bs4 import BeautifulSoup
except:
    print 'Vous devez installer le paquet python-bs4'


def apero():
    # TODO: recuperer l'interieur de la balise h2, il y a d'autres elements
    page = "http://estcequecestbientotlapero.fr"
    resultat = BeautifulSoup(requests.get(page).text)
    return resultat.font.string.encode('utf-8')

def weekend():
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"
