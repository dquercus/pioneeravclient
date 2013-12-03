__author__ = 'david'

import telnetlib
import socket

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

    def __init__(self, ip, port=8102, timeout=10):
        try:
            self.tn = telnetlib.Telnet(ip, port)
        except socket.timeout:
            raise PioneerAvClientException("Error connecting to device")

    def __sendcmd__(self, cmd):
        "Sends single command to AV"""
        command = cmd + '\r\n'
        
        self.tn.read_eager() # Cleanup any pending output.
        self.tn.write(command)
        sleep(0.1) # Cool-down time (taken from github/PioneerRebel)
        return self.tn.read_eager().replace('\r\n', '');

    def setVolUp(self):
        "Send request to increment volume by 1 unit"""
        self.__sendcmd__("VU")

    def setVolDown(self):
        "Send request to decrease volume by 1 unit"""
        self.__sendcmd__("VD")

    def isOn(self):
        "Returns true if device is on"""
        status = self.__sendcmd__("?P")
        
        if status == "PWR0":
            return True
        else:
            return False
        
    def switchOn(self):
        "Turn on device"""
        self.__sendcmd__("PO")
        sleep(5) # Wait before allowing any other command.

    def switchOff(self):
        "Turn off device"""
        self.__sendcmd__("PF")
        sleep(5) # Wait before allowing any other command.

    def mute(self):
        "Mute sound"""
        self.__sendcmd__("MO")

    def getVol(self):
        "Returns device volume in device scale 0-80"""
        vol_string = self.__sendcmd__("?V")
        vol_sub = vol_string[3:]
        return ( int(vol_sub) - 1 ) / 2

    def getVolPer(self):
        "Returns device volume in 0-100 scale"""
        vol = self.getVol( )
        vol_dec = float(vol) + 1.25
        return vol_dec
    
    def setInput(self, input_selector):
        "Send request to change input selector"""
        requested_input = input_selector+"FN"
        self.__sendcmd__(requested_input)
            
    def getInput(self):
        "Returns current input selector"""
        current_input_raw = self.__sendcmd__("?F")

        invd = { v:k for k,v in self.INPUTS.items() }

        try:
            return invd[current_input_raw[2:4]]
        except KeyError:
            raise PioneerAvClientException("Unknown input found " + current_input_raw)

    def close(self):
        self.tn.close()