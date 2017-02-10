import configparser

def readConf(section, parameter):
    config = configparser.RawConfigParser(allow_no_value=True)
    with open("settings.cfg", "r") as settings:
        config.read_file(settings)
    
    try:
        value = config.get(section, parameter)
    except Exception as err:
        print("Couldn't read conf file " + err)
        value = ""
    return value

