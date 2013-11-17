__author__ = 'david'

import telnetlib
from time import sleep

class PioneerAvClientException(Exception):
    pass

class VSX528Telnet(object):
    "Telnet client to Pioneer VSX-528 AV"""

    INPUTS = { "CD"           : "01",
               "TUNER"        : "02",
               "DVD"          : "04",
               "TV"           : "05",
               "SATCBL"       : "06",
               "VIDEO"        : "10",
               "DVR/BDR"      : "15",
               "IPOD/USB"     : "17",
               "BD"           : "25",
               "ADAPTER"      : "33",
               "NETRADIO"     : "38",
               "M.SERVER"     : "44",
               "FAVORITE"     : "45",
               "GAME"         : "49" }

    def __init__(self, ip, port=8102):
        try:
            self.tn = telnetlib.Telnet(ip, port)
        except EOFError:
            raise PioneerAvClientException("Error connecting to device")

    def __sendcmd__(self, cmd):
        "Sends single command to AV"""
        command = cmd + "\r\n"
        self.tn.write(command)
        sleep(0.1) # Cool-down time (taken from PioneerRebel


    def setVolUp(self):
        "Send request to increment volume by 1 unit"""
        self.__sendcmd__("VU")

    def setVolDown(self):
        "Send request to decrease volume by 1 unit"""
        self.__sendcmd__("VD")

    def mute(self):
        "Mute sound"""
        self.__sendcmd__("MO")

    def setInput(self, input_selector):
        "Send request to change input selector"""
        self.__sendcmd__(input_selector+"FN")
        current_input = self.tn.read_eager()

    def getInput(self):
        "Returns current input selector"""
        self.__sendcmd__("?F")
        current_input_raw = self.tn.read_eager()

        invd = { v:k for k,v in self.INPUTS.items() }

        try:
            return invd[current_input_raw[2:4]]
        except KeyError:
            raise PioneerAvClientException("Unknown input found " + current_input_raw)

    def close(self):
        self.tn.close()