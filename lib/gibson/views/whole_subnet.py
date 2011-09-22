# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 10:29:52 2011

@author: -
"""

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence, Parallel
from panda3d.core import Point3
from direct.showbase import DirectObject
from pandac.PandaModules import Thread
import random

class Panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.originals = {}
        blades = []
        servers = []
        self.setBackgroundColor(0.69,0.77,0.88)
        
        self.skybox = self.loader.loadModel("models/skysphere.egg")
        self.skyboxTexture = self.loader.loadTexture("images/floor.jpg")
        self.skyboxTexture.setWrapU(Texture.WMRepeat)     
        self.skyboxTexture.setWrapV(Texture.WMRepeat)        
        self.skybox.setTexture(self.skyboxTexture, 1)
        self.skybox.reparentTo(render)
        self.skybox.setScale(500)
        
        plight = PointLight('my plight')
        plight.setAttenuation(Point3(2, 0, 0))
        plnp = render.attachNewNode(plight)
        plnp.setPos(120, -320, 30)
        render.setLight(plnp)
        
        self.disableMouse()
        self.useDrive()
        base.drive.node().setPos(120, -320, 30)
        base.drive.node().setHpr(360, 0, 0)
        for i in range(16):
            blades.append(NodePath(str(i)))
            blades[i].show()
            blades[i].reparentTo(render)
            blades[i].setPos(i*15, 0, 0)
            blades[i].setColorScale(0, .8, 0, 1)
            blades[i].setTag('state', 'in')
            #blades[i].setScale(1, 4, 4)
            #blades[i].setTransparency(1)
            #blades[i].setColorScale(.2, .2, .2, .4)
            for j in range(16):
                this_server = self.loader.loadModel("models/low-cube.egg")
                servers.append(this_server)
                this_server.reparentTo(blades[i])
                y = (j % 4) * 10
                z = (int(j/4)) * 10
                this_server.setPos(0, y, z)
                this_server.setColorScale(0, .8, 0, 1)
                name = str(i) + "=" + str(j)
                this_server.setTag('myObjectTag', name)
                
        self.myHandler = CollisionHandlerQueue()
        self.myTraverser = CollisionTraverser()
        #base.cTrav = self.myTraverser
        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.myTraverser.addCollider(pickerNP, self.myHandler)
        
    def objectClicked(self):
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
 
        self.myTraverser.traverse(render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        if self.myHandler.getNumEntries() > 0:
            for i in range(self.myHandler.getNumEntries()):
                entry = self.myHandler.getEntry(i)
            self.myHandler.sortEntries()
            pickedObj = self.myHandler.getEntry(0).getIntoNodePath()
            pickedObj = pickedObj.findNetTag('myObjectTag')
            parent = pickedObj.getParent(Thread.getCurrentThread())
            if parent.getNetTag('state') == "in":
                self.AnimateOut(parent)
            elif parent.getNetTag('state') == "out":
                self.AnimateIn(parent)
                
                
    def AnimateOut(self, blade):
        x, y, z = blade.getPos()
        self.originals[blade] = (x, y, z)
        ending_position = (40 + random.uniform(0,120), y-(random.uniform(20,100)), z + random.uniform(-10,50))
        position1 = blade.posInterval(1, ending_position, (x, y, z))
        rotate1 = blade.hprInterval(1, (90, 0, 0), blade.getHpr())
        scale1 = blade.scaleInterval(1, (2, 2, 2), blade.getScale())
        move = Parallel(position1, rotate1, scale1, name="move")
        move.start()
        blade.setTag('state', 'out')
        
    def AnimateIn(self, blade):
        x, y, z = blade.getPos()
        ending_position = (self.originals[blade])
        position1 = blade.posInterval(1, ending_position, (x, y, z))
        rotate1 = blade.hprInterval(1, (0, 0, 0), blade.getHpr())
        scale1 = blade.scaleInterval(1, (1, 1, 1), blade.getScale())
        move = Parallel(position1, rotate1, scale1, name="move")
        move.start()
        blade.setTag('state', 'in')
                
class MouseClick(DirectObject.DirectObject):
    def __init__(self):
        self.accept('mouse1', self.leftClick)
        #self.accept('mouse3', self.rightClick)
    def leftClick(self):
        scene.objectClicked()
    #def rightClick(self):
        #scene.objectRightClicked()
                
scene = Panda()
m = MouseClick()
scene.run()
        
            
