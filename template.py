# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 17:14:34 2011

@author: -
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:58:20 2011

@author: -
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.showbase import DirectObject

import keyboard_events
import gui

class Panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0.69,0.77,0.88)
        self.dummy_center_node = render.attachNewNode("dummy_center_node")
        self.dummy_center_node.setPos(0, 0, 0)
        
        
        plight = PointLight('plnp')
        plight.setColor(VBase4(0.4, 0.4, 0.4, 1))
        plnp = self.render.attachNewNode(plight)
        plnp.setPos(-10, -160, 9)
        alight = AmbientLight('alnp')
        alight.setColor(VBase4(0.3, 0.3, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
        self.render.setLight(plnp)
        
        

        self.disableMouse()
        self.useDrive()        
        base.drive.node().setPos(0, -100, 9)
        base.drive.node().setHpr(355, 0, 0)
        base.drive.node().setIgnoreMouse(1)
        
        


        
        keys = keyboard_events.KeyboardEvents(base.drive.node(), self)
        #interface = gui.KeyboardEvents(keys, self.model, base.drive.node(), self)
        base.drive.node().setIgnoreMouse(1)
        
        self.myHandler = CollisionHandlerQueue()
        self.myTraverser = CollisionTraverser()
        self.myTraverser.setRespectPrevTransform(True)
        #self.myTraverser.showCollisions(render)
        #base.cTrav = self.myTraverser
        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.myTraverser.addCollider(pickerNP, self.myHandler)
        
        
    def objectClicked(self):
        pass
    def objectRightClicked(self):
        pass
        
        
        
        
        

class MouseClick(DirectObject.DirectObject):
    def __init__(self):
        self.accept('mouse1', self.leftClick)
        self.accept('space', self.leftClick)
        self.accept('mouse3', self.rightClick)
    def leftClick(self):
        scene.objectClicked()
    def rightClick(self):
        scene.objectRightClicked()







def startGibson(sceneClass=None):
    if sceneClass is None:
        scene = Panda()
    else:
        scene = sceneClass()
    m = MouseClick()
    globals()["scene"] = scene
    scene.run()






if __name__=="__main__":
    startGibson()
