# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:40:21 2010

@author: -
"""

import parse_nmap
import threedee_math
import slugger
import build
import keyboard_events
import gui
import build_subnet
import config
import node
import adhoc
import blades

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Fog
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
from optparse import OptionParser
import traceback

class Panda(ShowBase):
    def __init__(self, options):
        ShowBase.__init__(self)
        self.options = options
        if self.options.configfile:
            conf_file = self.options.configfile
        else:
            conf_file = 'None'
        configuration = config.ConfigFile(conf_file)
        self.new_node_counter = 0
        self.slugs = {}
        self.lasts = {}
        self.view = "hybrid"
        self.hybridview = NodePath("hybridview")
        self.hybridview.reparentTo(render)
        self.subnetview = NodePath("subnetview")
        self.subnetview.reparentTo(render)
        self.subnetview.hide()
        self.nodeview = NodePath("nodeview")
        self.nodeview.reparentTo(render)
        self.nodeview.hide()
        self.bladeview = NodePath("bladeview")
        self.bladeview.reparentTo(render)
        self.bladeview.hide()
        self.dummy_center_node = render.attachNewNode("dummy_center_node")
        self.dummy_center_node.setPos(0, 0, 0)
        self.camera.reparentTo(self.dummy_center_node)
        if configuration.bg_color():
            bg_color = configuration.bg_color()
            colors = bg_color.split(',')
            bg_color = (float(colors[0]), float(colors[1]), float(colors[2]))
        else:
            bg_color = (0.69,0.77,0.88)
        self.setBackgroundColor(bg_color)
        if configuration.skyshape():
            skybox_model = "models/" + configuration.skyshape()
        else:
            skybox_model = "models/skybox"
        try:

            self.skybox = self.loader.loadModel(skybox_model)
            
          
            #self.skybox.setScale(500) # make big enough to cover whole terrain, else there'll be problems with the water reflections
        
            #self.skybox.reparentTo(render) 
            #self.camLens.setFar(70)
           
        except:
            traceback.print_exc()
            print "Skybox Model not found"
        if configuration.skybox_texture():
            texture = "images/" + configuration.skybox_texture()
        else:
            texture="images/sky.jpg"
        try:
            self.skyboxTexture = self.loader.loadTexture(texture)
        except:
            print "Skybox texture not found."
            
        #self.skyboxTexture.setWrapU(Texture.WMRepeat)     
        #self.skyboxTexture.setWrapV(Texture.WMRepeat)        

        
    
        self.skybox.reparentTo(self.cam)
        #self.skybox.setScale(10)
        self.skybox.setScale(.01)
        self.skybox.setCompass()
        self.camLens.setFar(500)
        #myFog = Fog("Fog Name")
        #myFog.setColor(.8,.8,.8)
        #myFog.setExpDensity(.01)
        #myFog.setLinearRange(125,500)
        #myFog.setLinearFallback(4,160,320)
        #self.cam.attachNewNode(myFog)
        #render.setFog(myFog)
        #print self.skybox.getTightBounds()
        self.skybox.setTexture(self.skyboxTexture, 1)
        #self.skybox.setH(60)
        self.skybox.setBin('background', 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setLightOff()
          
        self.skybox.setCollideMask(BitMask32.allOff())

        
        self.disableMouse()
        self.useDrive()
        base.drive.node().setIgnoreMouse(1)
        
        base.drive.node().setPos(-10, -160, 9)
        base.drive.node().setHpr(340, 0, 0)
        plight = DirectionalLight('my plight')
        plnp = self.hybridview.attachNewNode(plight)
        plnp.setHpr(310, 0 ,30)
        self.hybridview.setLight(plnp)
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.4, 0.4, 0.4, 1))
        alnp = self.hybridview.attachNewNode(alight)
        self.hybridview.setLight(alnp)
        #keys = keyboard_events.KeyboardEvents(base.drive.node(), self)
        
        #self.model = build.BuildModel(self.options.configfile)
        #self.model.map_servers(self, parse_nmap.networkMap)
        #self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
        #self.low_x = {}
        #self.high_x = {}
        
        
        # Get Mouse Clicks
        self.myHandler = CollisionHandlerQueue()
        self.myTraverser = CollisionTraverser()
        self.myTraverser.setRespectPrevTransform(True)
        
        # Uncomment following line to make collisions (mouse clicks) visible on screen
        #self.myTraverser.showCollisions(render)
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
        keys = keyboard_events.KeyboardEvents(base.drive.node(), self)
        
        
        # Build the hybrid view (default) model
        if configuration.autobuild() == "true":
            self.model = build.BuildModel(self.options.configfile)
            self.model.map_servers(self, parse_nmap.networkMap)
            self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
            m = MouseClick()
            interface = gui.KeyboardEvents(keys, self.model, base.drive.node(), self)

            # Build the subnet view model
            self.subnet = build_subnet.BuildSubnetModel(base.drive.node(), self, conf_file)
        
        #self.hybridview.hide()
        #blade = blades.BladeView(self)
        
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                data = datagram.getMessage().split("|")
                id_builder = (data[1], data[3], data[4], data[5], data[6])
                id = "".join(id_builder)
                
                for i in self.model.master_zone_array:
                    for j in i:
                        if self.is_member_subnet(data[3], j.split()):
                            if data[3] not in self.model.servers:
                                print data[3] + "is in" + j
                                adhoc.NewServer(data[3], self)
                        if self.is_member_subnet(data[5], j.split()):
                            if data[5] not in self.model.servers:
                                print data[5] + "is in" + j
                                adhoc.NewServer(data[5], self)
                
                try:
                    self.slugs[id] = slugger.Slugger(self, data, self.subnet)
                except:
                    pass
                if self.view == "node" and self.single_node.IP == data[3]:
                    node_event = node.NodeEvent(data, self)
                
                
        return Task.cont
            
 

    
    def followCameraTask(self, task):

        #visible_range = {}
        
        #for k, v in self.model.servers.iteritems():
        #    v.show()
        return task.cont
       

        
        
    def moveSlugsTask(self, task):
        for k, v in self.slugs.iteritems():
            if self.view == "hybrid":
                self.slugs[k].pingpong.loop()
            
        return Task.cont
        
        
    def find_high_x(self, k, coords, visible_range, task):
        # These aren't currently used because, well, they don't work
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
        # Ditto
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
            print obj_id
            
            try:
                pickedObj2 = self.myHandler.getEntry(1).getIntoNodePath()
                obj_id2 = pickedObj2.getNetTag('myObjectTag')
                #print obj_id2
            except:
                pass
            
            try:
                pickedObj3 = self.myHandler.getEntry(2).getIntoNodePath()
                obj_id3 = pickedObj3.getNetTag('myObjectTag')
                #print obj_id3
            except:
                pass
            
            pickedObj = pickedObj.findNetTag('myObjectTag')
            if not pickedObj.isEmpty():
                if obj_id == "PopUp":
                    print "Pop Up"
                    if pickedObj.getAncestor(1).getNetTag("type") == "Tunnel":
                        pickedObj.removeNode()
                    else:
                        pickedObj.getAncestor(1).setScale(2)
                        pickedObj.removeNode()
                    
                elif obj_id == "ServerPopUp":
                    pickedObj.removeNode()
                elif (re.search("^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$", str(obj_id))):
                    self.findClickedServer(pickedObj, str(obj_id))
                else:
                    self.findClickedSlug(pickedObj, str(obj_id))
                    
    def objectRightClicked(self):
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
                if (re.search("^[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*$", str(obj_id))):
                    self.goToNodeView(pickedObj, str(obj_id))
                
        
             
                
    def findClickedSlug(self, slug, slug_id):
        for i in self.slugs.itervalues():
            match = ":".join(i.data[1:5])
            try:
                abc = i.node
            except:
                continue
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
                #self.popup.setScale(0.25)
                x, y, z = i.node.getPos()
                #self.popup.setPos(-3, 3, 3)
                self.popup.setTag('myObjectTag', 'PopUp')
                self.popup.setLightOff()
                if i.node.getNetTag('type') == "Tunnel":
                    self.popup.setPos(0.5, -10, 8)
                    self.popup.setScale(0.025, 0.05, 0.167)
                    self.popup.setColorScale(0, 0, 0, 0.9)
                    #self.popup.setBillboardAxis()
                    self.popup.setH(self.camera, 150)
                    self.popup.setCompass(self.camera)
                else:
                    self.popup.setScale(0.10)
                    self.popup.setPos(-3, 0, 3)
                    self.popup.setH(270)
                    #self.popup.setH(self.camera, 150)
                    #self.popup.setCompass(self.camera)
                    i.node.setScale(1.25)
                    
            
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
        
    def goToNodeView(self, original_object, IP):
        self.single_node = node.NodeView(self, IP, parse_nmap.networkMap[IP].services)
        self.view = "node"
        self.hybridview.hide()
        self.subnetview.hide()
        self.nodeview.show()
        
    def is_member_subnet(self, IP, subnets):
        try:
            if netaddr.all_matching_cidrs(IP, subnets):
                return True
        except:
            return False

    
    
class MouseClick(DirectObject.DirectObject):
    def __init__(self):
        self.accept('mouse1', self.leftClick)
        self.accept('space', self.leftClick)
        self.accept('mouse3', self.rightClick)
    def leftClick(self):
        scene.objectClicked()
    def rightClick(self):
        scene.objectRightClicked()
        
    
    
# Main
if __name__ == '__main__':
    option_parser = OptionParser()
    option_parser.add_option("-x", "--xml", dest="xmlfile", help="XMLFILE to use as input", metavar="XMLFILE")
    option_parser.add_option("-c", "--config", dest="configfile", help="read configuration from FILE", metavar="FILE")
    (options, args) = option_parser.parse_args()

    threedee_math = threedee_math.threedee_math()
    parser = xml.sax.make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = parse_nmap.ImportServer()
    parser.setContentHandler(dh)
    try:
        parser.parse(options.xmlfile)
    except:
        print "You have not specified an xml model. I'll assume you know what you're doing...."

    scene = Panda(options)
    scene.run()
