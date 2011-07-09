# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 09:58:11 2011

@author: -
"""

import parse_nmap
import threedee_math
import config

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
import sys

class BuildSubnetModel():
    def __init__(self, camera, panda, conf_file):
        if not conf_file:
            conf_file = 'None'
        self.configuration = config.ConfigFile(conf_file)
        self.camera = camera
        self.panda = panda
        self.view = self.panda.subnetview
        self.skybox = self.panda.loader.loadModel("models/skybox-big.egg")
        self.skyboxTexture = self.panda.loader.loadTexture("images/sky1.jpg")
        self.skyboxTexture.setWrapU(Texture.WMRepeat)     
        self.skyboxTexture.setWrapV(Texture.WMRepeat)        
        self.skybox.setTexture(self.skyboxTexture, 1)
        self.skybox.reparentTo(self.view)
        self.skybox.setScale(100)
        self.skybox.setH(60)

        
        plight = DirectionalLight('my plight')
        plnp = self.view.attachNewNode(plight)
        plnp.setHpr(310, 0 ,30)
        self.view.setLight(plnp)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.4, 0.4, 0.4, 1))
        alnp = self.view.attachNewNode(alight)
        self.view.setLight(alnp)
        
        self.threedee_math = threedee_math.threedee_math()
        self.master_zone_array = []
        self.security_zones = self.configuration.zone_list()
        print self.security_zones
        self.zone_list = self.security_zones.split(',')
        for i in self.zone_list:
            temp_array = self.configuration.subnet(i).split(',')
            self.master_zone_array.append(temp_array)
        self.x = {}
        for i in self.master_zone_array:
            self.x[self.master_zone_array.index(i)] = 0
        
        self.subnets = {}
        self.cidrs = {}
        self.map_subnets()
        
    def map_subnets(self):
        for i in self.master_zone_array:
            for j in i:
                self.place_subnet(i, j)
                
    def place_subnet(self, i, j):
        xcoord = 0
        ycoord = 0
        zcoord = 0
        subnet_number =  i.index(j)
        zone_number = self.master_zone_array.index(i)
        y = zone_number
        self.x[zone_number] = self.x[zone_number]+1
        xcoord = self.x[zone_number]
        ycoord = y
        zcoord = 8 * zone_number
        num = 2 * (zone_number + 1)
        red = float(float(num) % 10)/10.0
        tran = 1.0 - (float(y) / 10.0)
        basecolor = (red, 0.41, 0.80, tran)
        self.subnets[j] = self.panda.loader.loadModel("models/sphere.egg")
        self.subnets[j].reparentTo(self.panda.subnetview)
        self.subnets[j].setScale(5, 5, 5)
        self.subnets[j].setPos(xcoord*10, ycoord*(-24), zcoord)
        self.subnets[j].setTransparency(True)
        self.subnets[j].setColorScale(basecolor)
        self.subnets[j].setTag("myObjectTag", j)
        text = TextNode(j)
        text.setText(j)
        self.cidrs[j] = self.panda.subnetview.attachNewNode(text)
        self.cidrs[j].reparentTo(self.subnets[j])
        self.cidrs[j].setPos( -1.8, -1, 0)
        self.cidrs[j].setScale(.25, .25, .25)
        self.subnets[j].setH(330)
    
    
