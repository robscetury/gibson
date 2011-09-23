# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:36:44 2011

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
from gibson import threedee_math

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
from math import sin, cos, pi, sqrt, atan
import random

class ModelBase():
    def __init__(self, panda, nodes, radius = 5, center = None, scale = None):
        self.panda = panda
        self.nodes = {}
        self.slugs = {}
        if not center:
            self.center = self.panda.loader.loadModel(getPath("model","sphere.egg"))
            self.center.reparentTo(render)
            self.center.setColorScale(0.7, 0.41, 0.80, 1)
        else:
            self.center = center
        self._radius = radius
        self.scale = scale
        self.draw_nodes(nodes)

    def draw_nodes(self, number_of_nodes):
       
        number_of_nodes = float(number_of_nodes)
        pts = []
        inc = pi * (3 - sqrt(5))
        off = 2 / number_of_nodes
        
        for i in range(number_of_nodes):
            y = i * off - 1 + (off / 2)
            r = sqrt(1-y*y)
            phi = i * inc
            #step = 360 / number_of_nodes
            #degrees = degrees + step
            #radians = degrees * (pi / 180)
            self.nodes[i] = self.panda.loader.loadModel(getPath("model", "crt.egg"))
            if self.scale:
                self.nodes[i].setScale(self.scale)
            self.nodes[i].reparentTo(self.center)
            self.nodes[i].setPos(self._radius * (cos(phi)*r), self._radius*y, self._radius * (sin(phi)*r))
            
            self.nodes[i].setColorScale(0.5, 0.41, 0.80, 1)
            self.nodes[i].reparentTo(self.center)

class BuildModel(ModelBase):
    def __init__(self, panda, nodes):
        ModelBase.__init__(self, panda, nodes)
        
    def draw_nodes(self, number_of_nodes):
        number_of_nodes = float(number_of_nodes)
        pts = []
        inc = pi * (3 - sqrt(5))
        off = 2 / number_of_nodes
        
        ModelBase.draw_nodes(self, number_of_nodes)
        
            
        for i in range(30):
            self.slugs[i] = self.panda.loader.loadModel(getPath("model","slug2.egg"))
            parent = int(random.uniform(1,number_of_nodes))
            self.slugs[i].reparentTo(self.nodes[parent])
            self.slugs[i].setPos(-2, 0, 0)
            self.slugs[i].setScale(2, 2, 2)
            self.starting_position = self.nodes[parent].getPos()
            self.ending_position = (0, 0, 0)
            print self.starting_position
            print self.ending_position
            x, y, z = self.starting_position
            a, b, c = self.ending_position
            
            self.ending_position = (a-x, b-y, c-z)

            heading = atan(x/y * (180 / pi))
            roll = atan(z/x) * (180 / pi)
            #if z < 0:
            roll = roll * -1
            self.slugs[i].setH(heading)
            self.slugs[i].setR(roll)
            self.position1 = self.slugs[i].posInterval(60, self.starting_position, startPos=self.ending_position)
            self.position2 = self.slugs[i].posInterval(60, self.ending_position, startPos=self.starting_position)
            self.pingpong = Sequence(self.position1, self.position2, name=str(i))
            self.pingpong.loop()
            





