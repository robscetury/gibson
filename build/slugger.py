# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:31:22 2010

@author: -
"""
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

import netaddr

from math import pi, atan
import time
import random
import re


class Slugger():
    
    def __init__(self, panda, data, subnet):
        self.starting_position = (0, 0, 0)
        self.data = data
        self.panda = panda
        self.subnet = subnet
        print "got it"
        if self.data[6] == "22/tcp" or self.data[6] == "1521/tcp":
            self.createTunnel()
        elif self.data[3] in panda.model.servers and self.data[5] in panda.model.servers:
            self.createSlug("Intra")

        elif self.data[3] in panda.model.servers:
            self.createSlug("Outbound")
        
        elif self.data[5] in panda.model.servers:
            self.createSlug("Inbound")
        else:
            pass
            
    def createTunnel(self):
        parent = self.panda.model.servers[self.data[5]]
        
        self.node = self.panda.loader.loadModel("models/longslug.egg")
        self.node.reparentTo(parent)
        
        #parent.setColor(parent.getColor())
        self.node.setPos(-2, -10, -2)
        self.node.setScale(20, 10, 3)
        tag = ":".join(self.data[1:5])
        self.node.setTag('myObjectTag', tag)
        self.node.setTag('type', "Tunnel")
        self.node.setH(90)
        self.node.setColorScaleOff()
        self.node.setTransparency(1)
        if self.data[6] == "22/tcp":
            self.node.setColorScale(0, 0, 0, 0.7)
        if self.data[6] == "1521/tcp":
            self.node.setColorScale(0.76, 0.76, 0, 0.7)
            
    def createSlug(self, direction):
        if direction == "Intra":
            parent = self.panda.model.servers[self.data[3]]
        elif direction == "Outbound":
            parent = self.panda.model.servers[self.data[3]]
        elif direction == "Inbound":
            parent = self.panda.model.servers[self.data[5]]
        self.node = self.panda.loader.loadModel("models/slug2.egg")
        self.node.reparentTo(parent)
        self.node.setPos(-2, 0, 0)
        self.node.setScale(3, 3, 3)
        self.initial_position = self.node.getPos()
        if direction == "Intra":
            self.starting_position = self.initial_position
            self.ending_position = self.panda.model.servers[self.data[5]].getPos()
            x, y, z = self.panda.model.servers[self.data[3]].getPos()
        elif direction == "Outbound":
            x, y, z = self.initial_position
            self.starting_position = (x, y+random.uniform(0, 20), z)
            if self.data[4] == "N/A":
                ycoord = y-20
            else:
                ycoord = y-80
            self.ending_position = (x, ycoord, z)
        elif direction == "Inbound":
            x, y, z = self.initial_position
            self.starting_position = (x, (y-80)+random.uniform(0, 20), z)
            self.ending_position = (x, y, z)
        self.node.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node.setTag('myObjectTag', tag)
        if direction == "Intra":
            a, b, c = self.ending_position
            if b - y == 0:
                y = y+0.01
            self.ending_position = (a-x, b-y, c-z)
            if a-x == 0:
                x = 0.01
            heading = atan((a-x)/(b-y) * (180 / pi))
            roll = atan((c-z)/(a-x)) * (180 / pi)
            if c-z < 0:
                roll = roll * -1
            self.node.setH(heading)
            self.node.setR(roll)
            self.position1 = self.node.posInterval(60, self.ending_position, startPos=self.starting_position, fluid=1)
            self.position2 = self.node.posInterval(60, self.starting_position, startPos=self.ending_position, fluid=1)
            self.pingpong = Sequence(self.position1, self.position2, name=tag)
            #self.pingpong.loop()
        else:
            self.node.setH(90)
            self.position1 = self.node.posInterval(60, self.ending_position, startPos=self.starting_position, fluid=1)
            self.pingpong = Sequence(self.position1, name=tag)
        
        
                
                
        for k, net in self.subnet.subnets.iteritems():
            if self.is_member_subnet(self.data[3], k.split()):
                srcNet = net
            if self.data[5] == "N/A":
                dstNet = ""
            elif self.is_member_subnet(self.data[5], k.split()):
                dstNet = net
        if direction == "Intra":
            parent = srcNet
        elif direction == "Outbound":
            parent = srcNet
        elif direction == "Inbound":
            parent = dstNet
        self.node1 = self.panda.loader.loadModel("models/slug2.egg")
        self.node1.reparentTo(parent)
        self.node1.setPos(-2, 0, 0)
        self.node1.setScale(1, 1, 1)
        self.initial_position = self.node1.getPos()
        if direction == "Intra":
            self.starting_position = self.initial_position
            self.ending_position = dstNet.getPos()
            x, y, z = srcNet.getPos()
            a, b, c = dstNet.getPos()
        elif direction == "Outbound":
            x, y, z = self.initial_position
            self.starting_position = (x+2, y+random.uniform(0, 20), z)
            if self.data[4] == "N/A":
                ycoord = y-20
            else:
                ycoord = (y-50)+random.uniform(0, 20)
            self.ending_position = (x, ycoord, z)
        elif direction == "Inbound":
            x, y, z = self.initial_position
            self.starting_position = (x, y-50, z)
            self.ending_position = (x, y, z)
        


        
        
        self.node1.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node1.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node1.setTag('myObjectTag', tag)
        if direction == "Intra":
            
            if a - x == 0:
                x = x+0.01
            self.ending_position = (a-x, b-y, c-z)
            
            
            heading = atan((b-y)/(a-x)) * (180 / pi)
            roll = atan((c-z)/(a-x)) * (180 / pi)
            if c-z < 0:
                roll = roll * -1
            self.node1.setH(heading)
            self.node1.setR(roll)
            self.position3 = self.node1.posInterval(60, self.ending_position, startPos=self.starting_position)
            self.position4 = self.node1.posInterval(60, self.starting_position, startPos=self.ending_position)
            self.pingpong1 = Sequence(self.position3, self.position4, name=tag)
            #self.pingpong1.loop()
        else:
            self.node1.setH(90)
            self.position3 = self.node1.posInterval(60, self.ending_position, startPos=self.starting_position)
            self.pingpong1 = Sequence(self.position3, name=tag)
            #self.pingpong1.loop()
            
        if self.panda.view == "hybrid":
            
            self.pingpong.loop()
        elif self.panda.view == "subnet":
            self.pingpong1.loop()
   
        
    def is_member_subnet(self, IP, subnets):
        if netaddr.all_matching_cidrs(IP, subnets):
            return True
        return False
