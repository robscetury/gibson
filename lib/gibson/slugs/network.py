# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:31:22 2010

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
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

import netaddr

from math import pi, atan
import time
import random
import re
from gibson.slugs import SluggerBase
from gibson import *


def createSlug(panda, data, subnet):
    if data[6] == "22/tcp" or data[6] == "1521/tcp":
        return Tunnel(panda,data,subnet)
    elif data[3] in panda.model.servers and data[5] in panda.model.servers:
        return IntraSlug(panda,data,subnet)
    elif data[3] in panda.model.servers:
        return OutboundSlug(panda,data,subnet)

    elif data[5] in panda.model.servers:
        return InboundSlug(panda,data,subnet)
    else:
            pass
class NetworkSlug(SluggerBase):
    
    def __init__(self, panda, data, subnet):
        SluggerBase.__init__(self, panda, data)
        self.subnet = subnet
        self.node = self.panda.loader.loadModel(getPath("model", "slug2.egg"))
        self.data = data
        #print "got it"

    def is_member_subnet(self, IP, subnets):
        if netaddr.all_matching_cidrs(IP, subnets):
            return True
        return False

class Tunnel(NetworkSlug):
    def __init__(self, panda, data, subnet):
        NetworkSlug.__init__(self,panda, data,subnet)
        parent = self.panda.model.servers[self.data[5]]

        self.node = self.panda.loader.loadModel(getPath("model", "longslug.egg"))
        self.node.reparentTo(parent)

        #parent.setColor(parent.getColor())
        self.node.setPos(-2, -10, -2)
        self.node.setScale(5, 2.5, .75)
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
        if self.data[2] == "SensitiveConnection":
            self.node.setColor(0.76, 0, 0, 1)


class IntraSlug(NetworkSlug):
    def __init__(self,panda,data,subnet):
        NetworkSlug.__init__(self, panda, data, subnet)
        parent = self.panda.model.servers[self.data[3]]
        self.node.reparentTo(parent)
        self.node.setPos(-2, 0, 0)
        self.node.setScale(.75, .75, .75)
        self.node.getParent().setScale(5)
        self.node.getParent().setAlphaScale(0.9)
        self.initial_position = self.node.getPos()
        print "Intra"
        self.starting_position = self.initial_position
        self.ending_position = self.panda.model.servers[self.data[5]].getPos()
        x, y, z = self.panda.model.servers[self.data[3]].getPos()
        print "Going from" + str(x) + " " + str(y) + " "  + str(z)
        print "To" + str(self.ending_position)
        self.node.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node.setTag('myObjectTag', tag)
        dt = time.time()
        self.node.setTag('createTime', str(dt))


        a, b, c = self.ending_position
        if b - y == 0:
             y = y+0.01
        #self.ending_position = ((a/4)-x, (b-y)/4, (c-z)/4)
        print str(self.ending_position)
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
        dstNet = ""
        for k, net in self.subnet.subnets.iteritems():
            if self.is_member_subnet(self.data[3], k.split()):
                srcNet = net
                if self.data[5] == "N/A":
                    dstNet = ""
                elif self.is_member_subnet(self.data[5], k.split()):
                    dstNet = net
        parent = srcNet
        self.node1 = self.panda.loader.loadModel(getPath("model", "slug3.egg"))
        self.node1.reparentTo(parent)
        self.node1.setPos(0, 0, 0)
        self.node1.setScale(.2, .2, .2)
        self.initial_position = self.node1.getPos()
        #print self.initial_position
        self.starting_position = self.initial_position
        self.ending_position = dstNet.getPos()
        self.ending_position = dstNet.getPos()
        x, y, z = srcNet.getPos()
        a, b, c = dstNet.getPos()

        self.node1.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node1.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node1.setTag('myObjectTag', tag)
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

        if self.panda.view == "hybrid":

            self.pingpong.loop()
        elif self.panda.view == "subnet":
            self.pingpong1.loop()




class OutboundSlug(NetworkSlug):

    def __init__(self, panda, data, subnet):
        NetworkSlug.__init__(self,panda,data,subnet)
        parent = self.panda.model.servers[self.data[3]]
        self.node = self.panda.loader.loadModel(getPath("model", "slug3.egg"))
        self.node.reparentTo(parent)
        self.node.setPos(0, 0, 0)
        self.node.setScale(.75, .75, .75)
        self.node.getParent().setScale(5)
        self.node.getParent().setAlphaScale(0.9)
        self.initial_position = self.node.getPos()
        self.node = self.panda.loader.loadModel(getPath("model", "slug3.egg"))
        self.node.reparentTo(parent)
        self.node.setPos(0, 0, 0)
        self.node.setScale(.75, .75, .75)
        self.node.getParent().setScale(5)
        self.node.getParent().setAlphaScale(0.9)
        self.initial_position = self.node.getPos()
        x, y, z = self.initial_position
        self.starting_position = (x, y+random.uniform(0, 20), z)
        if self.data[4] == "N/A":
            ycoord = y-20
        else:
            ycoord = y-80
        self.ending_position = (x, ycoord, z)
        self.node.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node.setColor(0.76, 0, 0, 1)
            #parent.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node.setTag('myObjectTag', tag)
        dt = time.time()
        self.node.setTag('createTime', str(dt))
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
        parent = srcNet

        self.node1 = self.panda.loader.loadModel(getPath("model","slug3.egg"))
        self.node1.reparentTo(parent)
        self.node1.setPos(0, 0, 0)
        self.node1.setScale(.2, .2, .2)
        self.initial_position = self.node1.getPos()
        #print self.initial_position
        self.node1 = self.panda.loader.loadModel(getPath("model","slug3.egg"))
        self.node1.reparentTo(parent)
        self.node1.setPos(0, 0, 0)
        self.node1.setScale(.2, .2, .2)
        self.initial_position = self.node1.getPos()
        #print self.initial_position
        x, y, z = self.initial_position
        self.starting_position = (x+2, y+random.uniform(0, 20), z)
        if self.data[4] == "N/A":
            ycoord = y-20
        else:
            ycoord = (y-50)+random.uniform(0, 20)
        self.ending_position = (x, ycoord, z)

        self.node1.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node1.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node1.setTag('myObjectTag', tag)
        self.node1.setH(90)
        self.position3 = self.node1.posInterval(60, self.ending_position, startPos=self.starting_position)
        self.pingpong1 = Sequence(self.position3, name=tag)
        #self.pingpong1.loop()

        if self.panda.view == "hybrid":

            self.pingpong.loop()
        elif self.panda.view == "subnet":
            self.pingpong1.loop()

class InboundSlug(NetworkSlug):
    def __init__(self, panda, data, subnet):
        NetworkSlug.__init__(self, panda, data, subnet)
        parent = self.panda.model.servers[self.data[5]]
        self.node = self.panda.loader.loadModel(getPath("model", "slug3.egg"))
        self.node.reparentTo(parent)
        self.node.setPos(0, 0, 0)
        self.node.setScale(.75, .75, .75)
        self.node.getParent().setScale(5)
        self.node.getParent().setAlphaScale(0.9)
        self.initial_position = self.node.getPos()
        x, y, z = self.initial_position
        self.starting_position = (x, (y-80)+random.uniform(0, 20), z)
        self.ending_position = (x, y, z)
        self.node.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node.setColor(0.76, 0, 0, 1)
            #parent.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node.setTag('myObjectTag', tag)
        dt = time.time()
        self.node.setTag('createTime', str(dt))
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
        parent = dstNet
        #print parent
        self.node1 = self.panda.loader.loadModel(getPath("model", "slug3.egg"))
        self.node1.reparentTo(parent)
        self.node1.setPos(0, 0, 0)
        self.node1.setScale(.2, .2, .2)
        self.initial_position = self.node1.getPos()
        #print self.initial_position
        x, y, z = self.initial_position
        self.starting_position = (x, y-50, z)
        self.ending_position = (x, y, z)



        
        
        self.node1.setTransparency(1)
        if self.data[2] == "SensitiveConnection":
            self.node1.setColor(0.76, 0, 0, 1)
        tag = ":".join(self.data[1:5])
        self.node1.setTag('myObjectTag', tag)
        self.node1.setH(90)
        self.position3 = self.node1.posInterval(60, self.ending_position, startPos=self.starting_position)
        self.pingpong1 = Sequence(self.position3, name=tag)
        #self.pingpong1.loop()
            
        if self.panda.view == "hybrid":
            
            self.pingpong.loop()
        elif self.panda.view == "subnet":
            self.pingpong1.loop()
   
        