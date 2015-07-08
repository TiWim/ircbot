#! /usr/env/python

print "implemented: apero, weekend"




def apero():
    page = "http://estcequecestbientotlapero.fr"
    resultat = requests.get(page).text
    regex = re.compile('<font size=5>(.*)</font>').search(resultat)
    return regex.group(1)

def weekend():
    page = "http://estcequecestbientotleweekend.fr"
    resultat = requests.get(page).text
    regex = re.compile('<font size=5>(.*)</font>').search(resultat)
    return regex.group(1)



