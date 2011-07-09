# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 15:13:02 2011

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
        info = TextNode('sign1')
        text = open('alarm.sign')
        info.clearTextColor()
        info.setText(text.read())
        info.setCardAsMargin(0, 0, 0.5, 0)
        info.setCardColor(1.0, 1.0, 1.0, 0.4)
        info.setTextColor(1.0, 0.0, 0.0, 0.7)
        info.setFrameAsMargin(0, 0, 0.5, 0)
        info.setFrameColor(0.0, 0.0, 0.0, .9)
        info.setCardDecal(True)
        clickable = info.generate()
        self.popup = self.panda.hybridview.attachNewNode(clickable)
        self.popup.setH(30)
        self.popup.setScale(0.5)
        self.popup.setPos(-10, -45, 15)
        self.popup.setTag('myObjectTag', 'PopUp')
        self.popup.setLightOff()
        text.close()
        
        info2 = TextNode('sign2')
        text = open('syslog.sign')
        info2.clearTextColor()
        info2.setText(text.read())
        info2.setCardAsMargin(0, 0, 0.5, 0)
        info2.setCardColor(1.0, 1.0, 1.0, 0.4)
        info2.setTextColor(1.0, 0.0, 0.0, 0.7)
        info2.setFrameAsMargin(0, 0, 0.5, 0)
        info2.setFrameColor(0.0, 0.0, 0.0, .9)
        info2.setCardDecal(True)
        clickable2 = info2.generate()
        self.popup2 = self.panda.hybridview.attachNewNode(clickable2)
        self.popup2.setH(30)
        self.popup2.setScale(0.5)
        self.popup2.setPos(-5, -50, 20)
        self.popup2.setTag('myObjectTag', 'PopUp')
        self.popup2.setLightOff()
        text.close
        
        info3 = TextNode('sign3')
        text = open('gdb.sign')
        info3.clearTextColor()
        info3.setText(text.read())
        info3.setCardAsMargin(0, 0, 0.5, 0)
        info3.setCardColor(1.0, 1.0, 1.0, 0.4)
        info3.setTextColor(1.0, 0.0, 0.0, 0.7)
        info3.setFrameAsMargin(0, 0, 0.5, 0)
        info3.setFrameColor(0.0, 0.0, 0.0, .9)
        info3.setCardDecal(True)
        clickable3 = info3.generate()
        self.popup3 = self.panda.hybridview.attachNewNode(clickable3)
        self.popup3.setH(30)
        self.popup3.setScale(0.5)
        self.popup3.setPos(0, -55, 25)
        self.popup3.setTag('myObjectTag', 'PopUp')
        self.popup3.setLightOff()
        text.close
        
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
        position1 = self.popup3.posInterval(2, (20, -70, 25),startPos=self.popup3.getPos() )
        rotate1 = self.popup3.hprInterval(2, (0, 0, 0), self.popup3.getHpr())
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
        
