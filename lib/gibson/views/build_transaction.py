# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 11:12:49 2011

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
import threedee_math

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.showbase import DirectObject

import netaddr

import os
import socket
import operator
from math import sin, cos, pi, sqrt, atan
import random
from gibson import getPath

class BuildModel():
    def __init__(self, panda, ip_array):
        self.panda = panda
        self.nodes = {}
        self.slugs = {}
        self.positions = []
        self.intervals = []
        
        self.slug = self.panda.loader.loadModel(getPath("model", "slug2.egg"))
        self.slug.reparentTo(render)
        self.slug.setTransparency(1)
        self.slug.setColorScale(0.8, 0.2, 0.2, 1)
        self.slug.setScale(4, 3, 3)
        
        for ip in ip_array:
            self.nodes[ip] = self.panda.loader.loadModel(getPath("model","crt.egg"))
            self.nodes[ip].reparentTo(render)
            x = ip_array.index(ip)*-30
            y = 0
            z = 0
            self.nodes[ip].setPos(x, y, z)
            
            self.nodes[ip].setTransparency(1)
            self.nodes[ip].setColorScale (0.5, 0.5, 0.8, 1)
            if ip_array.index(ip) == 0:
                starting_position = (x+30, y, z)
                self.positions.append((x, y, z))
            
            else:
                idx = ip_array.index(ip) - 1
                print idx
                starting_position = self.positions[idx]
                self.positions.append((x, y, z))
            print ip
            print str(starting_position) + " to " + str(self.nodes[ip].getPos())
            self.intervals.append (self.slug.posInterval(10, self.nodes[ip].getPos(), startPos = Point3(starting_position)))
        
        
            
        #pos1 = self.slugs[ip].posInterval(10, Point3(0, 0, 0), startPos=Point3(30, 0, 0))
        #pos2 = self.slugs[ip].posInterval(10, Point3(-30, 0, 0), startPos=Point3(0, 0, 0))
        #pos3 = self.slugs[ip].posInterval(10, Point3(-60, 0, 0), startPos=Point3(-30, 0, 0))
        self.pingpong = Sequence(name="pingpong")
        for i in self.intervals:
            self.pingpong.append(i)
        self.pingpong.loop()
            
            
                
        
            
            
