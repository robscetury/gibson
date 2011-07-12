# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 16:45:20 2011

@author: -
"""
import threedee_math

import netaddr

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.showbase import DirectObject

import socket

class NewServer():
    def __init__(self, IP, panda):
        print "NewServer"
        self.threedee_math = threedee_math.threedee_math()
        self.panda = panda
        self.IP = IP
        self.x = {}
        
        
        self.panda.model.servers[IP] = True
        print "Building node for" + IP
        
        for i in self.panda.model.master_zone_array:
            for j in i:
                self.x[j] = 0
                
        self.panda.model.servers[IP] = self.panda.loader.loadModel("models/crt.egg")
        self.rearrangeServers()
        print self.panda.new_node_counter
        
    def rearrangeServers(self):
        new_one = False
        sorted_servers = sorted(self.panda.model.servers.iteritems(), key=lambda x: int(x[0].split(".").pop()))
        for k, v in sorted_servers:
            for i in self.panda.model.master_zone_array:
                for j in i:
                    self.subnet_number =  i.index(j)
                    self.zone_number = self.panda.model.master_zone_array.index(i)
                    if self.is_member_subnet(k, j.split()):
                        self.x[j] = self.x[j]+1
                        if new_one and self.is_member_subnet(self.IP, j.split()):
                            v.setX(v.getX()+10)
                        if k == self.IP:
                            print "Node loop " + k
                            self.buildNew(k, self.x[j])
                            new_one = True
                
    def buildNew(self, IP, x):
        self.panda.new_node_counter = self.panda.new_node_counter+1
        #self.panda.model.servers[IP].reparentTo(self.panda.hybridview)
        #self.panda.model.servers[IP].setX(-50)
        xcoord = 0
        ycoord = 0
        zcoord = 0
        
        z = self.subnet_number-2
        y = self.zone_number
        xcoord = x
        ycoord = y
        zcoord = z
        offset = 8 * self.zone_number
        #red = 0.1 + 2*((float(zone_number)+1)/10)
        num = 2 * (self.zone_number + 1)
        red = float(float(num) % 10)/10.0
        tran = 1.0 - (float(y) / 10.0)
        basecolor = (red, 0.41, 0.80, tran)
                
        
        coords = xcoord*10, ycoord*(-26), zcoord*14
        
        self.panda.model.servers[IP].reparentTo(self.panda.hybridview)
        self.panda.model.servers[IP].setScale(4, 4, 4)
        self.panda.model.servers[IP].setPos(xcoord*10, ycoord*(-26), zcoord*14+offset)
        self.panda.model.servers[IP].setTransparency(True)
        self.panda.model.servers[IP].setColorScale(basecolor)
        self.panda.model.servers[IP].setTag("myObjectTag", IP)
        print self.panda.model.servers[IP].getPos()
        
        text = TextNode(IP)
        try:
            hostname = socket.gethostbyaddr(IP)[0]
        except socket.herror:
            hostname = "Unknown"
        os = "Unknown"
        text.setText(hostname[:8] + "\n" + IP + "\n" + os)
        self.panda.model.names[IP] = self.panda.hybridview.attachNewNode(text)
        self.panda.model.names[IP].reparentTo(self.panda.model.servers[IP])
        self.panda.model.names[IP].setPos( -1.8, -1.5, 1.5)

        
        distance = self.threedee_math.distance_between(base.drive.node().getPos(), coords)
        if distance > 250:
            self.panda.model.servers[IP].hide()
            self.panda.model.names[IP].hide()
        
        
    def is_member_subnet(self, IP, subnets):
        if netaddr.all_matching_cidrs(IP, subnets):
            return True
        return False
