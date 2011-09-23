# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 15:13:02 2011

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
#import parse_nmap
from gibson  import threedee_math
from gibson import config


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
import random


class Sign():
    def __init__(self, panda):
        self.panda = panda
        signs = [(TextNode('sign1'))]
        clickables = []
        self.popups = []
        for sign in signs:
            num = signs.index(sign)
            text = open(str(num))
            sign.clearTextColor()
            sign.setText(text.read())
            sign.setCardAsMargin(0, 0, 0.5, 0)
            sign.setCardColor(1.0, 1.0, 1.0, 0.4)
            sign.setTextColor(1.0, 0, 0, 1.0)
            sign.setFrameAsMargin(0, 0, 0.5, 0)
            sign.setFrameColor(0, 0, 0, 0.9)
            sign.setCardDecal(True)
            clickables.append(sign.generate())
            self.popups.append(self.panda.hybridview.attachNewNode(clickables[num]))
            self.popups[num].setH(30)
            self.popups[num].setScale(0.5)
            self.popups[num].setPos(-10 + 5*num, -45 + 5*num, 15 + 5*num)
            self.popups[num].setTag('myObjectTag', 'PopUp')
            self.popups[num].setLightOff()
            text.close()
            
        model_sign = self.panda.loader.loadModel("models/sign.egg")
        model_sign.reparentTo(self.panda.hybridview)
        model_sign.setPos(0, -100, 10)
        model_sign.setH(90)
        model_sign_text = TextNode('model_sign_text')
        model_sign_text.setTextColor(0, 0, 0, 1)
        sign_text = ("Hello, world!")
        model_sign_text.setText(sign_text)
        text_node = model_sign.attachNewNode(model_sign_text)
        text_node.setPos(-0.5, 1.8, 0)
        text_node.setH(-90)
        text_node.setScale(.6, .6, .6)
        
        
        
        signlight = PointLight('signlight')
        signlight.setColor(VBase4(0.4, 0.4, 0.4, 1))
        slnp = self.panda.hybridview.attachNewNode(signlight)
        slnp.setPos(-20, -5, 0)
        #model_sign.setLightOff()
        
            
            
        
        
        other_sign = TextNode('block')
        text = "Hostile IP\nblocked"
        other_sign.clearTextColor()
        other_sign.setText(text)
        other_sign.setTextColor(1.0, 0.0, 0.0, 1.0)
        self.popup4 = self.panda.render.attachNewNode(other_sign)
        self.popup4.setPos(50, -75, 20)
        self.popup4.setScale(2, 2, 2)
        a = self.popup4.colorScaleInterval(0.5, (0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 1.0))
        b = self.popup4.colorScaleInterval(0.5, (1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 0.0))
        self.x = Sequence(a,Func(self.blinkOn),b)
        self.x.loop()
        
    def moveSign(self):
        position1 = self.popups[0].posInterval(2, (20, -70, 25),startPos=self.popups[0].getPos() )
        rotate1 = self.popups[0].hprInterval(2, (0, 0, 0), self.popups[0].getHpr())
        par = Parallel(position1, rotate1, name="blah")
        par.start()
        
    def blinkOn(self):
        x, y, z = self.popup4.getPos()
        x = x + random.uniform(-20, 20)
        z = z + random.uniform(-10, 10)
        self.popup4.setPos(x, y, z)
        a = random.uniform(1,10)
        if int(a) == 9:
            self.popup4.setPos(50, -75, 20)
        
    def blinkOff(self):
        self.popup4.hide()
        
