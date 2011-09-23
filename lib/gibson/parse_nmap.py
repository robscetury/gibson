# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 19:31:57 2010

@author: -
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
import xml.sax
from xml.sax.handler import feature_namespaces, ContentHandler
import string

networkMap = {}

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())



class ImportServer(ContentHandler):
    def __init__(self):
        self.inHost = 0
        self.inIPaddress = 0
        self.inPort = 0
        
    def startElement(self, name, attrs):
        global networkMap
        if name == 'host':
            self.inHost = 1
        if self.inHost and name == 'address' and attrs.get('addrtype', "") == 'ipv4':
            self.inIPaddress = 1
            self.IPaddress = attrs.get('addr', "")
            networkMap[self.IPaddress] = Server()

        if self.inHost and name == 'port':
            self.inPort = 1
            self.Port = attrs.get('portid', "")
            self.Proto = attrs.get('protocol', "")
        if self.inHost and name == 'osclass':
            networkMap[self.IPaddress].osclass = attrs.get('osfamily', "")
        if self.inHost and self.inPort:
            if name == 'state' and attrs.get('state', "") == 'open':
                self.Service = self.Port, self.Proto
        
            
 
            
    def endElement(self, name):
        global networkMap
        if name == 'port':
            self.inPort = 0
            try:
                if self.Service:
                #print self.Service
                    self.Service = self.Port, self.Proto
                    networkMap[self.IPaddress].services.append(self.Service)

            
                self.Service = ()
                self.Port = ""
                self.Proto = ""
            except:
                pass
            
        if name == 'address':
            self.inIPaddress = 0
            
        if name == 'host':
            self.IPaddress = ""
            self.inHost = 0
            

class Server():
    def __init__(self):
        self.services = []
        self.services.append((0, 'ipv4'))
        self.osclass = "unknown"
    
    
    
if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = ImportServer()
    parser.setContentHandler(dh)
    parser.parse('home.xml')
    for k, v in networkMap.iteritems():
        print k,v
