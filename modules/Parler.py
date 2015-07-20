#! /usr/env/python
import requests
import re
print "implemented: apero, weekend"


def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<font size=5>(.*)</font>', resultat).group(1)
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"

def weekend():
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    try:
        return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()
    except:
        print "exception"  # print stacktrace
        return "Une erreur s'est produite"
