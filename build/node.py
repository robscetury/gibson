# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:02:35 2011

@author: -
"""

import parse_nmap
import threedee_math
import config
import random

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from panda3d.core import Point3
from direct.showbase import DirectObject

import netaddr

import os
import socket
import operator
import sys

class NodeView():
    def __init__(self, panda, IP, services):
        self.IP = IP
        self.panda = panda
        self.services = services
        self.apps = {}
        self.app_info = {}
        self.app_names = {}
        
        if sys.argv[1]:
            conf_file = sys.argv[2]
        else:
            conf_file = 'None'
        configuration = config.ConfigFile(conf_file)
        
        self.skybox = self.panda.loader.loadModel("models/skybox.egg")
        texture = "images/" + configuration.skybox_texture()
        self.skyboxTexture = self.panda.loader.loadTexture(texture)
        self.skybox.setTexture(self.skyboxTexture, 1)
        self.skybox.reparentTo(self.panda.nodeview)
        self.skybox.setScale(500)
        self.skybox.setH(60)
        
        plight = PointLight('my plight')
        plight.setAttenuation(Point3(1, 0, 0))
        plnp = self.panda.nodeview.attachNewNode(plight)
        plnp.reparentTo(self.panda.camera)
        self.panda.nodeview.setLight(plnp)
        self.panda.dummy_center_node.setH(0)
        self.panda.dummy_center_node.setPos(0, 0, 0)
        self.panda.camera.setPos(-10, -75, 10)
        self.panda.camera.setHpr(90, 0, 0)
        self.main_node = self.panda.loader.loadModel("models/low-cube.egg")
        self.main_node.reparentTo(panda.nodeview)
        self.main_node.setScale(4, 4, 8)
        self.main_node.setTransparency(1)
        self.main_node.setColorScale(0.4, 0.2, 0.7, 0.4)
        self.main_node.setPos(30, 0, 0)
        for service in services:
            self.apps[service] = self.panda.loader.loadModel("models/drawer.egg")
            self.apps[service].reparentTo(self.main_node)
            self.apps[service].setScale(1, 1, 0.8)
            z = (services.index(service)-2)
            self.apps[service].setPos(1.5, 0, z)
            self.apps[service].setTransparency(0)
            self.apps[service].clearColor()
            self.apps[service].setColorScale(1, 0.4, 0.7, 1.0)
            self.app_info[service] = TextNode(str(service))
            portnum = int(service[0])
            protocol = service[1].encode('ascii', 'ignore')
            print str(portnum) + " " + protocol
            try:
                srvname = socket.getservbyport(portnum, protocol)
            except:
                srvname = "unknown"
            self.app_info[service].setText(srvname + "\n" + str(portnum) + "/" + protocol)
            self.app_names[service] = self.apps[service].attachNewNode(self.app_info[service])
            self.app_names[service].setPos(-3, -5, 0)
            self.app_names[service].setScale(0.25, 0.25, 0.25)
            self.app_names[service].setColor(0, 0, 0)
            
        text = TextNode(IP)
        try:
            hostname = socket.gethostbyaddr(IP)[0]
        except socket.herror:
            hostname = "Unknown"
        
        text.setText(hostname[:8] + "\n" + IP + "\n")
        self.name = self.main_node.attachNewNode(text)
        #self.names[IP].reparentTo(servers[IP])
        self.name.setPos( 0, 3, 5.5)
        self.name.setScale(0.5, 0.5, 0.5)
        self.name.setColor(0, 0, 0, 1)
        self.name.setTransparency(0)
        
        text2 = TextNode('2')
        text2.setText(text.getText())
        self.name2 = self.main_node.attachNewNode(text2)
        self.name2.setPos( 0, 3, -5)
        self.name2.setScale(0.5, 0.5, 0.5)
        self.name2.setColor(0, 0, 0)
        self.name2.setTransparency(0)
        self.looper = Parallel(name="looper")
            
class NodeEvent():
    def __init__(self, data, panda):
        self.data = data
        self.panda = panda
        service = data[7].split("[")
        #self.blinks = {}
        print service[0]
        try:
            port = socket.getservbyname(service[0])
            print port
        except:
            port = ""
        if service[0] == "init":
            col1 = self.panda.single_node.main_node.colorScaleInterval(1, (1, 1, 0, 0.7), (0.4, 0.2, 0.7, 0.4))
            col2 = self.panda.single_node.main_node.colorScaleInterval(1, (0.4, 0.2, 0.7, 0.4), (1, 1, 0, 0.7))
            col3 = self.panda.single_node.main_node.colorScaleInterval(5, (0.4, 0.2, 0.7, 0.4), (0.4, 0.2, 0.7, 0.4))
            blink = Sequence(col1, col2, col3, name="blink")
            #blink.loop()
        for i in self.panda.single_node.services:
            print ":" + str(i[0]) + ":" + str(port) + ":"
            if str(i[0]) == str(port):
                print "match"
                self.panda.single_node.apps[i].setColorOff()
                col1 = self.panda.single_node.apps[i].colorScaleInterval(1, (1, 1, 0, 1), (1, 0.4, 0.7, 1.0))
                col2 = self.panda.single_node.apps[i].colorScaleInterval(1, (1, 0.4, 0.7, 1.0), (1, 1, 0, 1))
                col3 = self.panda.single_node.apps[i].colorScaleInterval(2, (random.uniform(1,3), 0.4, 0.7, 1.0), (1, 0.4, 0.7, 1.0))
                blink = Sequence(col1, col2, col3, name="blink")
                #self.blinks[port].loop()
        #looper = Parallel(name="looper")
        try:
            self.panda.single_node.looper.append(blink)
        except:
            pass
        
        self.panda.single_node.looper.loop()

        
        
