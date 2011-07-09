# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 11:10:36 2011

@author: -
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:40:21 2010

@author: -
"""

import parse_nmap
import threedee_math
import slugger
import keyboard_events
import gui
import build_transaction

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.showbase import DirectObject

import netaddr

from math import pi, sin, cos
import sys
import xml.sax
from xml.sax.handler import feature_namespaces, ContentHandler
import string
import os
import socket
import re



class Panda(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.slugs = {}
        self.lasts = {}
        self.view = "hybrid"
        self.hybridview = NodePath("hybridview")
        self.hybridview.reparentTo(render)
        self.subnetview = NodePath("subnetview")
        self.subnetview.reparentTo(render)
        self.subnetview.hide()
        self.dummy_center_node = render.attachNewNode("dummy_center_node")
        self.dummy_center_node.setPos(0, 0, 0)
        self.setBackgroundColor(0.69,0.77,0.88)
        self.skybox = self.loader.loadModel("models/skysphere.egg")
        self.skyboxTexture = self.loader.loadTexture("images/book.jpg")
        self.skyboxTexture.setWrapU(Texture.WMRepeat)     
        self.skyboxTexture.setWrapV(Texture.WMRepeat)        

        self.skybox.setTexture(self.skyboxTexture, 1)
        self.skybox.reparentTo(self.hybridview)
        self.skybox.setScale(500)
        self.skybox.setH(60)

        
        self.disableMouse()
        self.useDrive()
        base.drive.node().setPos(-30, -100, 0)
        base.drive.node().setHpr(0, 0, 0)
        plight = PointLight('my plight')
        plnp = self.render.attachNewNode(plight)
        plnp.reparentTo(render)
        plnp.setPos(0, -100, 5)
        #plnp.setHpr(310, 0 ,30)
        #self.hybridview.setLight(plnp)
        render.setLight(plnp)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.4, 0.4, 0.4, 1))
        alnp = self.hybridview.attachNewNode(alight)
        self.hybridview.setLight(alnp)
        keys = keyboard_events.KeyboardEvents(base.drive.node(), self)
        ip_array = ['128.5.72.14', '192.168.1.23', '10.1.1.42']
        self.model = build_transaction.BuildModel(self, ip_array)
        self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
        
            
        # Get Mouse Clicks
        self.myHandler = CollisionHandlerQueue()
        self.myTraverser = CollisionTraverser()
        pickerNode = CollisionNode('mouseRay')
        pickerNP = camera.attachNewNode(pickerNode)
        pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        pickerNode.addSolid(self.pickerRay)
        self.myTraverser.addCollider(pickerNP, self.myHandler)
        
        
        
        # Receive events
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        activeConnections=[]
        udpSocket = self.cManager.openUDPConnection(1723)
        self.cReader.addConnection(udpSocket)
        self.taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        
        # Create GUI and switch modes / views
        interface = gui.KeyboardEvents(keys, self.model, base.drive.node(), self)
        
        #self.subnet = build_subnet.BuildSubnetModel(base.drive.node(), self)
        #messenger.send('start-loop')
        
        
        
        
        
        
        
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                data = datagram.getMessage().split("|")
                id_builder = (data[1], data[3], data[4], data[5], data[6])
                id = "".join(id_builder)
                try:
                    self.slugs[id] = slugger.Slugger(self, data, self.subnet)
                except:
                    raise
                
                
        return Task.cont
            
 

    
    def followCameraTask(self, task):
        return Task.cont
        
        
    def find_high_x(self, k, coords, visible_range, task):
        for i in self.model.subnet_list:
            if self.model.is_member_subnet(k, i.split()):
                if coords[0] < visible_range[i][0]:
                    visible_range[i] = (coords[0], visible_range[i][1])
                if coords[0] > visible_range[i][1]:
                    visible_range[i] = (visible_range[i][0], coords[0])
        for i in self.model.private_net_list:
            if self.model.is_member_subnet(k, i.split()):
                if coords[0] < visible_range[i][0]:
                    visible_range[i] = (coords[0], visible_range[i][1])
                if coords[0] > visible_range[i][1]:
                    visible_range[i] = (visible_range[i][0], coords[0])
                    
    def find_low_x(self, k, coords, visible_range, task):
        for i in self.model.subnet_list:
            if self.model.is_member_subnet(k, i.split()):
                if coords[0] > visible_range[i][0]:
                    visible_range[i] = (coords[0], visible_range[i][1])
                if coords[0] < visible_range[i][1]:
                    visible_range[i] = (visible_range[i][0], coords[0])
                    
        for i in self.model.private_net_list:
            if self.model.is_member_subnet(k, i.split()):
                if coords[0] > visible_range[i][0]:
                    visible_range[i] = (coords[0], visible_range[i][1])
                if coords[0] < visible_range[i][1]:
                    visible_range[i] = (visible_range[i][0], coords[0])
                    
                    
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
            obj_id = pickedObj.getNetTag('myObjectTag')
            pickedObj = pickedObj.findNetTag('myObjectTag')
            if not pickedObj.isEmpty():
                if obj_id == "PopUp":
                    pickedObj.getAncestor(1).setScale(2)
                    pickedObj.removeNode()
                elif obj_id == "ServerPopUp":
                    pickedObj.removeNode()
                elif (re.search("^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$", str(obj_id))):
                    self.findClickedServer(pickedObj, str(obj_id))
                else:
                    self.findClickedSlug(pickedObj, str(obj_id))
        
             
                
    def findClickedSlug(self, slug, slug_id):
        for i in self.slugs.itervalues():
            match = ":".join(i.data[1:5])
            if (match == slug_id):
                info = TextNode(str(slug_id))
                text = "\n".join(i.data[1:])
                info.clearTextColor()
                info.setText(text)
                info.setCardAsMargin(0, 0, 0.5, 0)
                info.setCardColor(1.0, 1.0, 1.0, 0.7)
                info.setTextColor(1.0, 0.0, 0.0, 1.0)
                info.setFrameAsMargin(0, 0, 0.5, 0)
                info.setFrameColor(0.0, 0.0, 0.0, .9)
                info.setCardDecal(True)
                clickable = info.generate()
                self.popup = self.hybridview.attachNewNode(clickable)
                self.popup.reparentTo(i.node)
                self.popup.setH(270)
                self.popup.setScale(0.25)
                x, y, z = i.node.getPos()
                self.popup.setPos(-3, 3, 3)
                self.popup.setTag('myObjectTag', 'PopUp')
                self.popup.setLightOff() 
                i.node.setScale(3)
            
    def findClickedServer(self, server, IP):
        info = TextNode(IP)
        try:
            hostname = socket.gethostbyaddr(IP)[0]
        except socket.herror:
            hostname = "Unknown"
        os = parse_nmap.networkMap[IP].osclass
        text = hostname[:8] + "\n" + IP + "\n" + os
        for i in parse_nmap.networkMap[IP].services:
            text += "\n" + str(i[0]) + "/" + str(i[1])
        print text
        info.setText(text)        
        info.setCardAsMargin(0, 0, 0.5, 0)
        info.setCardColor(1.0, 1.0, 1.0, 0.7)
        info.setTextColor(0.0, 0.0, 0.0, 1.0)
        info.setFrameAsMargin(0, 0, 0.5, 0)
        info.setFrameColor(0.0, 0.0, 0.0, .9)
        info.setCardDecal(True)
        clickable = info.generate()
        self.popup = self.hybridview.attachNewNode(clickable)
        self.popup.reparentTo(server)
        #self.popup.setH(270)
        #self.popup.setScale(0.5)
        self.popup.setPos(-3, -5, 0)
        self.popup.setTag('myObjectTag', 'ServerPopUp')
        self.popup.setLightOff() 

    
    
class MouseClick(DirectObject.DirectObject):
    def __init__(self):
        self.accept('mouse1', self.printHello)
    def printHello(self):
        scene.objectClicked()
        
    
    
# Main
#print os.environ['local_nets']
threedee_math = threedee_math.threedee_math()


scene = Panda()
m = MouseClick()



scene.run()
