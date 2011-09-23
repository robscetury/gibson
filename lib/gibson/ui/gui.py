# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 10:13:04 2011

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
import keyboard_events

from direct.showbase import DirectObject
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pandac.PandaModules import Thread

import socket
import re


class KeyboardEvents(DirectObject.DirectObject):
    def __init__(self, keys, model, camera, panda):
        self.keys = keys
        self.model = model
        self.camera = camera
        self.mode = "MOVE"
        self.panda = panda
        self.accept('escape', self.escapePressed)
        self.accept('tab', self.tabPressed)
        self.accept('start-loop', self.startLoop)
        self.accept('shift-=', self.speedUp)
        self.accept('shift-=-repeat', self.speedUp)
        self.accept('-', self.slowDown)
        self.accept('--repeat', self.slowDown)

    def speedUp(self):
        #print "Speedin up"
        for slug in self.panda.slugs.itervalues():
            try:
                slug.pingpong.setPlayRate(slug.pingpong.getPlayRate()*1.5)
                slug.pingpong1.setPlayRate(slug.pingpong.getPlayRate()*1.5)
            except:
                pass

    def slowDown(self):
        for slug in self.panda.slugs.itervalues():
            try:
                slug.pingpong.setPlayRate(slug.pingpong.getPlayRate()*0.5)
                slug.pingpong1.setPlayRate(slug.pingpong.getPlayRate()*0.5)
            except:
                pass


        #self.mode = "MOVE"
        
    def tabPressed(self):
        if self.panda.view == "hybrid":
            self.switchToSubnet()
        elif self.panda.view == "subnet":
            self.switchToHybrid()
        elif self.panda.view == "node":
            self.panda.single_node.main_node.removeNode()
            self.switchToHybrid()
            
    def switchToSubnet(self):
        self.panda.hybridview.hide()
        self.panda.view = "subnet"
        self.panda.subnetview.show()
        self.camera.setPos(0, -160, 5)
        self.panda.dummy_center_node.setH(0)
        self.camera.setH(340)
        print "start pingpong1"
        try:
            for i in self.panda.slugs.itervalues():
                print "moving"
                try:
                    i.pingpong1.resume()
                except:
                    print "not moving"
                
        except:
            print "Starting slugs failed"

        
    def switchToHybrid(self):
        self.camera.setPos(0, -160, 9)
        self.panda.dummy_center_node.setH(0)
        self.camera.setH(340)
        self.panda.subnetview.hide()
        self.panda.hybridview.show()
        
        self.panda.view = "hybrid"
        print "start pingpong"
        try:
            for i in self.panda.slugs.itervalues():
                print "moving"
                try:
                    i.pingpong.resume()
                except:
                    print "not moving"
                
        except:
            pass
            
    def startLoop(self):
        try:
            for i in self.panda.slugs.itervalues():
                if self.panda.view == "hybrid":
                    i.pingpong.loop()
                elif self.panda.view == "subnet":
                    i.pingpong1.loop()
                else:
                    pass
        except:
            pass
        
    def escapePressed(self):
        if self.mode == "GUI":
            self.closeGUI()
        elif self.mode == "MOVE":
            self.openGUI()
            
    def closeGUI(self):
        self.my_gui.search_field.destroy()
        self.mode = "MOVE"
        self.keys.accept('w', self.keys.Levitate)
        self.keys.accept('s', self.keys.Down)
        self.keys.accept('w-repeat', self.keys.Levitate)
        self.keys.accept('s-repeat', self.keys.Down)
        self.keys.accept('q', self.keys.Left)
        self.keys.accept('e', self.keys.Right)
        self.keys.accept('x', self.keys.Original)
        self.keys.accept('a', self.keys.spinLeft)
        self.keys.accept('a-repeat', self.keys.spinLeft)
        self.keys.accept('d', self.keys.spinRight)
        self.keys.accept('d-repeat', self.keys.spinRight)
        
    def openGUI(self):
        self.my_gui = MyGUI(self.model, self.camera, self, self.panda)
        print "Disabling keys"
        self.keys.ignore('w')
        self.keys.ignore('w-repeat')
        self.keys.ignore('s')
        self.keys.ignore('s-repeat')
        self.keys.ignore('q')
        self.keys.ignore('e')
        self.keys.ignore('x')
        self.keys.ignore('a')
        self.keys.ignore('a-repeat')
        self.keys.ignore('d')
        self.keys.ignore('d-repeat')
        self.mode = "GUI"
        #self.my_gui = MyGUI(self.model, self.camera, self)
        
    
        
        
        
class MyGUI:
    def __init__(self, model, camera, kbd, panda):
        self.model = model
        self.camera = camera
        self.kbd = kbd
        self.panda = panda
        
        self.search_field = DirectEntry(text = "" ,scale=.05,command=self.search, initialText="", numLines = 1,focus=1)
        
        
        
        
    def search(self, text):
        if re.search("^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$",text):
            ip = text
        else:
            try:
                ip = socket.gethostbyname(text)
            except socket.gaierror:
                print "not found"
                ip = ""
        if ip in self.model.servers:
            (x, y, z) = self.model.servers[ip].getPos()
            (a, b, c) = self.camera.getPos()
            self.panda.dummy_center_node.setPos((x-a)-3, (y-b)-24, (z-c)+3)
            self.panda.dummy_center_node.setH(0)
        else:
            print "not found"
            
        
        self.search_field.destroy()
        self.closeGUI()
        
        
        
    def closeGUI(self):
        self.kbd.escapePressed()
        
