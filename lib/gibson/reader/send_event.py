# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 12:04:32 2010

@author: -
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task

import sys


class EncapsulateForPanda():
    
    def __init__(self):
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        self.myConnection = self.cManager.openUDPConnection()
        
    def send_event(self, host, port, alert_text):
        target = NetAddress()
        target.setHost(host, port)
        payload = NetDatagram()
        payload.addString(alert_text)
        self.cWriter.send(payload, self.myConnection, target)
        

if __name__ == '__main__':
    sender = EncapsulateForPanda()
    sender.send_event(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    


