#! /usr/env/python
import requests
import re
print "implemented: apero, weekend"




def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = requests.get(page).text
    return re.search('<font size=5>(.*)</font>', resultat).group(1)



def weekend():
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    return re.search('<p class="msg">(.*?)</p>', resultat, re.DOTALL).group(1).strip()

