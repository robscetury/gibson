# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 11:29:42 2011

@author: -
"""
import threedee_math
import sign

from direct.showbase import DirectObject
from math import pi, sin, cos, atan


class KeyboardEvents(DirectObject.DirectObject):
    def __init__(self, camera, panda):
        self.threedee_math = threedee_math.threedee_math()
        self.camera = camera
        self.panda = panda
        self.orientation = "landscape"
        self.accept('y', self.Levitate)
        self.accept('y-repeat', self.Levitate)
        self.accept('h', self.Down)
        self.accept('h-repeat', self.Down)
        self.accept('q', self.spinLeft)
        self.accept('q-repeat', self.spinLeft)
        self.accept('e', self.spinRight)
        self.accept('e-repeat', self.spinRight)
        self.accept('x', self.Original)
        
        self.accept('z', self.slideLeft)
        self.accept('z-repeat', self.slideLeft)
        self.accept('c', self.slideRight)
        self.accept('c-repeat', self.slideRight)
        self.accept('shift-z', self.slideLeftFast)
        self.accept('shift-z-repeat', self.slideLeftFast)
        self.accept('shift-c', self.slideRightFast)
        self.accept('shift-c-repeat', self.slideRightFast)
        self.accept('r', self.tiltForward)
        self.accept('r-repeat', self.tiltForward)
        self.accept('f', self.tiltBack)
        self.accept('f-repeat', self.tiltBack)
        self.accept('b', self.jumpBack)
        self.accept('g', self.jumpUp)
        self.accept('t', self.rotateScene)
        self.accept('p', self.exampleSigns)
        self.accept('l', self.exampleMove)
        self.accept('o', self.exampleKill)
        
        self.accept('w', self.Forward)
        self.accept('w-repeat', self.Forward)
        self.accept('s', self.Backward)
        self.accept('s-repeat', self.Backward)
        self.accept('a', self.rotateLeft)
        self.accept('a-repeat', self.rotateLeft)
        self.accept('d', self.rotateRight)
        self.accept('d-repeat', self.rotateRight)
        
    def rotateScene(self):
        print self.orientation
        if self.orientation == "landscape":
            if self.panda.view == "hybrid":
                self.panda.hybridview.setR(90)
                self.camera.setPos(-20, -100, 50)
                self.camera.setP(-50)
                for i in self.panda.model.names.itervalues():
                    i.setR(-90)
                    i.setZ(i.getZ()-1.5)
                    i.setColorScaleOff()
                    i.setColorScale(0, 0, 0, 1)
                self.orientation = "portrait"
                
        elif self.orientation == "portrait":
            if self.panda.view == "hybrid":
                self.panda.hybridview.setR(0)
                self.camera.setPos(-10, -160, 10)
                self.camera.setP(0)
                for i in self.panda.model.names.itervalues():
                    i.setR(0)
                    #i.setX(i.getX()+10)
                    i.setZ(i.getZ()+1.5)
                    i.setColorScaleOff()
                    i.setColorScale(0, 0, 0, 1)
                self.orientation = "landscape"
        
    def Levitate(self):
        (x, y, z) = self.camera.getPos()
        self.camera.setPos(x, y, z+1)
        
    def Forward(self):
        (h, p, r) = self.camera.getHpr()
        (x, y, z) = self.camera.getPos()
        h = h + 90
        h = h * (pi / 180)
        p = p * (pi / 180)
        self.camera.setPos(x+(5*cos(h)), y+(5*sin(h)), z+(5*sin(p)))
        
    def Backward(self):
        (h, p, r) = self.camera.getHpr()
        (x, y, z) = self.camera.getPos()
        h = h + 90
        h = h * (pi / 180)
        p = p * (pi / 180)
        self.camera.setPos(x-(5*cos(h)), y-(5*sin(h)), z-(5*sin(p)))
        
    def rotateLeft(self):
        self.camera.setH(self.camera.getH()+1)
        
    def rotateRight(self):
        self.camera.setH(self.camera.getH()-1)
        
    def Down(self):
        (x, y, z) = self.camera.getPos()
        self.camera.setPos(x, y, z-1)
        
    def Left(self):
        self.camera.setPos(-30, -30, 12)
        self.camera.setH(270)
    def slideLeft(self):
        (x, y, z) = self.camera.getPos()
        self.camera.setPos(x-1, y, z)
    def slideRight(self):
        (x, y, z) = self.panda.dummy_center_node.getPos()
        self.panda.dummy_center_node.setPos(x+1, y, z)
    def slideLeftFast(self):
        (x, y, z) = self.camera.getPos()
        self.camera.setPos(x-10, y, z)
    def slideRightFast(self):
        (x, y, z) = self.camera.getPos()
        self.camera.setPos(x+10, y, z)
    def Right(self):
        self.camera.setPos(200, -30, 12)
        self.camera.setH(90)
    def Original(self):
        self.camera.setPos(0, -160, 9)
        self.camera.setHpr(340, 0, 0)
        
    def spinLeft(self):
        (x, y, z) = self.camera.getPos()
        (h, p, r) = self.camera.getHpr()
        self.panda.camera.reparentTo(self.panda.dummy_center_node)
        
        self.panda.dummy_center_node.setH(self.panda.dummy_center_node.getH() - 1)
        
    def spinRight(self):
        (x, y, z) = self.camera.getPos()
        (h, p, r) = self.camera.getHpr()
        self.panda.camera.reparentTo(self.panda.dummy_center_node)
        self.panda.dummy_center_node.setH(self.panda.dummy_center_node.getH() + 1)
        
        
    def tiltForward(self):
        current = self.camera.getP()
        self.camera.setP(current-1)
    def tiltBack(self):
        current = self.camera.getP()
        self.camera.setP(current+1)
    def jumpBack(self):
        self.camera.setY(-500)
        
    def jumpUp(self):
        (h, p, r) = self.camera.getHpr()
        (x, y, z) = self.camera.getPos()
        h = h + 90
        h = h * (pi / 180)
        p = p * (pi / 180)
        self.camera.setPos(x+(100*cos(h)), y+(100*sin(h)), z+(100*sin(p)))
        
    def exampleSigns(self):
        self.signage = sign.Sign(self.panda)
        
    def exampleMove(self):
        try:
            self.signage.moveSign()
        except:
            pass
        
    def exampleKill(self):
        for i in self.signage.popups:
            i.removeNode()
        
        
        self.signage.x.finish()
        self.signage.popup4.removeNode()
