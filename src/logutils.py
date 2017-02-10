# -*- coding: utf-8 -*-

import time

log_fileName = "bot.log"
log_file = open(log_fileName, "a")


def logs(message, author="", info="info"):
    print time.strftime("%m-%d %H:%M:%S"), info, author + ":", message
    log_file.write(time.strftime("%m-%d %H:%M:%S") + " " + message + "\n")
