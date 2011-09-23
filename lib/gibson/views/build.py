# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 16:26:49 2011

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
from gibson import parse_nmap
from gibson import threedee_math
from gibson import config


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.showbase import DirectObject

import netaddr
from gibson import *
import os
import socket
import operator
import sys
from gibson import getPath

class BuildModel():
    def __init__(self, conf_file):
        if not conf_file:
            conf_file = 'None'
        self.configuration = config.ConfigFile(conf_file)
        self.threedee_math = threedee_math.threedee_math()
        self.master_zone_array = []
        self.security_zones = self.configuration.zone_list()
        print self.security_zones
        self.zone_list = self.security_zones.split(',')
        for i in self.zone_list:
            temp_array = self.configuration.subnet(i).split(',')
            self.master_zone_array.append(temp_array)
        
        self.x = {}
        self.servers = {}
        self.names = {}

        for i in self.master_zone_array:
            for j in i:
                self.x[j] = 0
       
    def map_routers(self, conf_file):
        routers = self.configuration.routers()
        for i in routers:
            print i
            
    def map_servers(self, panda, server_list):
        x = 0
        
        sorted_servers = sorted(parse_nmap.networkMap.iteritems(), key=lambda x: int(x[0].split(".").pop()))
        for k, v in sorted_servers:
            self.place_server(panda, x, k, self.servers)
            x = x + 1
    
    def place_server(self, panda, counter, IP, servers):
        xcoord = 0
        ycoord = 0
        zcoord = 0
        for i in self.master_zone_array:
            for j in i:
                subnet_number =  i.index(j)
                zone_number = self.master_zone_array.index(i)
                if self.is_member_subnet(IP, j.split()):
                    z = subnet_number-2
                    y = zone_number
                    self.x[j] = self.x[j]+1
                    xcoord = self.x[j]
                    ycoord = y
                    zcoord = z
                    offset = 8 * zone_number
                    #red = 0.1 + 2*((float(zone_number)+1)/10)
                    num = 2 * (zone_number + 1)
                    red = float(float(num) % 10)/10.0
                    #tran = 6.0 - (float(y) / 20.0)
                    tran = 0.7
                    basecolor = (red, 0.41, 0.60, tran)
                
        
        coords = xcoord*10, ycoord*(-24), zcoord*12
        servers[IP] = panda.loader.loadModel(getPath("model", "crt.egg"))
        servers[IP].reparentTo(panda.hybridview)
        servers[IP].setScale(4, 4, 4)
        servers[IP].setPos(xcoord*10, ycoord*(-24), zcoord*12+offset)
        servers[IP].setTransparency(True)
        servers[IP].setColorScale(basecolor)
        servers[IP].setTag("myObjectTag", IP)
        
        if parse_nmap.networkMap[IP].osclass == "Mac OS X":
            finalcolor = (basecolor[0], basecolor[1]+0.2, basecolor[2]+0.2, basecolor[3])
        elif parse_nmap.networkMap[IP].osclass == "Linux":
            finalcolor = (basecolor[0], basecolor[1]-0.1, basecolor[2]+0.1, basecolor[3])
        elif parse_nmap.networkMap[IP].osclass == "Windows":
            finalcolor = (basecolor[0], basecolor[1]-0.2, basecolor[2]-0.2, basecolor[3])
        elif parse_nmap.networkMap[IP].osclass == "Solaris":
            finalcolor = (basecolor[0], basecolor[1]+0.1, basecolor[2]-0.1, basecolor[3])
        else:
            finalcolor = basecolor
        servers[IP].setColorScale(finalcolor)
            
        text = TextNode(IP)
        try:
            hostname = socket.gethostbyaddr(IP)[0]
        except socket.herror:
            hostname = "Unknown"
        os = parse_nmap.networkMap[IP].osclass
        text.setText(hostname[:8] + "\n" + IP + "\n" + os)
        self.names[IP] = panda.hybridview.attachNewNode(text)
        self.names[IP].reparentTo(servers[IP])
        self.names[IP].setPos( -1.8, -1.5, 1.5)
        self.names[IP].setScale(.25, .25, .25)

        
        distance = self.threedee_math.distance_between(base.drive.node().getPos(), coords)
        
        #if distance > 200:
            #servers[IP].setPos(xcoord*10-2, ycoord-2, zcoord*12+offset)
            #servers[IP].setH(315)
            #self.names[IP].setPos(servers[IP], 3, -5.5, 2.5)
            #self.names[IP].setH(0)
            #text.setAlign(TextNode.ABoxedRight)
        #if distance > 250:
        #    servers[IP].hide()
        #    self.names[IP].hide()
        
    
    def is_member_subnet(self, IP, subnets):
        if netaddr.all_matching_cidrs(IP, subnets):
            return True
        return False
    
