"""
This file will:
 1) load and launch the reader (in gibson/reader/) or readers(!) specified by the configuration file
 2) load and launch the specified handler [this handles messages incoming from the UI]

 Changes from current (0.0003 release):
 1) Readers must be threads
 2) Readers working off stdin must handle that on their own

"""
#Copyright 2011 Dan Klinedinst
#
#This file is part of Gibson.
#
#Gibson is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation, either version 3 of the License, or any
#later version.

#Gibson is distributed in the hope that it will be useful, but WITHOUT
#ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License
#along with Gibson.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'rob'


from twisted.protocols.basic import NetstringReceiver
from hmac import HMAC
from xml.dom import minidom

class UnableToConnectToDatabase(Exception):
    pass

class CredentialFailure(Exception):
    pass

class EventClient(NetstringReceiver):

    def __init__(self, queue, ipaddr = None, port = None, password=None, username=None):
        NetstringReceiver.__init__(self)
        self.queue = queue
        if ipaddr is None:
            pass
            #read in from config/settings

        self.ipaddr = ipaddr

        if port is None:
            pass
            #read in from config/settings
        if password:
            self._password = HMAC(password)
        else:
            self._password = ""
        if username:
            self._username = username
        else:
            self._username = username
        self._auth = None
    def connectionMade(self):
        self.sendString("LOGIN %s %s"%(self._username, self._password))

    def stringReceived(self, string):
        try:
            d = minidom.parseString(string)
            self.handleXML(d)
        except:
            self.handleNONXML(string)


    def handleXML(self, d):
        callingDict = dict()
        argDict = dict()
        for methNode in d.documentElement.childNodes:
            callingDict[ methNode.nodeName] = argDict
            for child in d.documentElement.childNodes:
                argDict[child.nodeName] = child.lastNode.nodeValue
        self.queue.put(callingDict)


    def handleNONXML(self, string):
        stack = string.split(" ")
        command = stack[0]
        if command == "auth" and not self._auth:
            self._auth = stack[1]
        elif command == "auth" and self._auth:
            raise "Error: Received second auth token!"
        elif command =="FAILURE" and not self._auth:
            if stack[1] == "DB_UNAVAILABLE":
                raise UnableToConnectToDatabase()
            else:
                raise CredentialFailure()
        else:
            if self._auth:
                if command == "READER":
                    self.scene = self.loadScene(stack[1])
                elif command == "USERS":
                    userList = stack[1].split(",")
                    self.scene.userList = userList


    def sendPosition(self, x, y, z, h, p, r):
        username = self._username
        auth = self._auth
        string = """<position>
                <username>%(username)s</username>
                <x>%(x)s</x>
                <y>%(y)s</y>
                <z>%(z)s</z>
                <h>%(h)s</h>
                <p>%(p)s</p>
                <r>%(r)s</r>
                <auth>%(auth)s</auth>"""%locals()
        self.sendString(self, string)