#! /usr/env/python
# coding: utf-8

import requests
import re
try:
    from bs4 import BeautifulSoup
except:
    print 'Vous devez installer le paquet python-bs4'


def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = BeautifulSoup(requests.get(page).text)
    return resultat.h2.text.encode('utf-8').replace(".", ". ").strip()

def weekend():
    # TODO verify the format of this site
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"
