# -*- coding: utf-8 -*-
import configparser
import codecs
def readConf(section, parameter):
    config = configparser.RawConfigParser(allow_no_value=True)
    config.readfp(codecs.open("settings.cfg", 'r', 'utf-8'))
#    with config.readfp(open("settings.cfg", "r", "utf-8") as settings:
#        config.read_file(settings)
    try:
        value = config.get(section, parameter).encode("utf-8")
    except Exception as err:
        print("Couldn't read conf file " + err)
        value = ""
    return value

