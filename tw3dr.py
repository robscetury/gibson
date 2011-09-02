import template
from panda3d.core import Fog
from physics import *
from pandac.PandaModules import *
from direct.task import Task
import build_cluster 
import slugger
import random
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

import netaddr

from math import pi, atan
import time
import random
import re
class Tweet(slugger.SluggerBase):
    def __init__(self,panda, data):
        slugger.SluggerBase.__init__(self, panda, data)
        self.createSlug("Inbound")
        
    def createSlug(self, direction):
        #print u"creating slug for @%s"%self.data[3]
        parentName = str("@%s"%self.data[3])
        parent = self.panda.friends.get(parentName.strip())
        dest = self.panda.dummy_center_node
        if not parent:
            parent = self.panda.followers.get(parentName.strip())
                
        if parent:
            #print parent
            self.node = self.panda.loader.loadModel("models/slug2.egg")
            self.node.reparentTo(parent)
            self.node.setPos(parent.getPos())
            #self.node.setScale(.75, .75, .75)
            #self.node.getParent().setScale(5)
            #self.node.getParent().setAlphaScale(0.9)
            self.initial_position = self.node.getPos()
            #print "got node"
            if direction == "Intra":
                #print "Intra"
                self.starting_position = self.initial_position
                self.ending_position = dest.getPos()
                x, y, z = self.panda.nodes["@%s"%self.data[3]].getPos()
                #print "Going from" + str(x) + " " + str(y) + " "  + str(z)
                #print "To" + str(self.ending_position)
            elif direction == "Outbound":
                x, y, z = self.initial_position
                self.starting_position = (x, y+random.uniform(0, 20), z)
                if self.data[4] == "N/A":
                    ycoord = y-20
                else:
                    ycoord = y-80
                self.ending_position = (x, ycoord, z)
            elif direction == "Inbound":
                x, y, z = self.initial_position
                #self.starting_position = (x, (y-80)+random.uniform(0, 20), z)
                self.ending_position = dest.getPos()
            self.node.setTransparency(1)
            if self.data[2] == "SensitiveConnection":
                self.node.setColor(0.76, 0, 0, 1)
                #parent.setColor(0.76, 0, 0, 1)
            tag = self.data[4]
            self.node.setTag('myObjectTag', tag)
            if direction == "Intra":
                a, b, c = self.ending_position
                if b - y == 0:
                    y = y+0.01
                self.ending_position = ((a/4)-x, (b-y)/4, (c-z)/4)
                #print str(self.ending_position)
                if a-x == 0:
                    x = 0.01
                heading = atan((a-x)/(b-y) * (180 / pi))
                roll = atan((c-z)/(a-x)) * (180 / pi)
                if c-z < 0:
                    roll = roll * -1
                self.node.setH(heading)
                self.node.setR(roll)
                self.position1 = self.node.posInterval(30, self.ending_position, startPos=self.starting_position, fluid=1)
                self.position2 = self.node.posInterval(30, self.starting_position, startPos=self.ending_position, fluid=1)
                self.pingpong = Sequence(self.position1, self.position2, name=tag)
                #self.pingpong.loop()
            else:
                self.node.setH(90)
                self.position1 = self.node.posInterval(30, self.ending_position, startPos=self.starting_position, fluid=1)
                self.pingpong = Sequence(self.position1, name=tag)
            self.node1 = self.panda.loader.loadModel("models/slug2.egg")
            self.node1.reparentTo(parent)
            self.node1.setPos(-2, 0, 0)
            #self.node1.setScale(.2, .2, .2)
            self.initial_position = self.node1.getPos()
            #print self.initial_position
            if direction == "Intra":
                self.starting_position = self.initial_position
                self.ending_position = dstNet.getPos()
                x, y, z = srcNet.getPos()
                a, b, c = dstNet.getPos()
            elif direction == "Outbound":
                x, y, z = self.initial_position
                self.starting_position = (x+2, y+random.uniform(0, 20), z)
                if self.data[4] == "N/A":
                    ycoord = y-20
                else:
                    ycoord = (y-50)+random.uniform(0, 20)
                self.ending_position = (x, ycoord, z)
            elif direction == "Inbound":
                #print "Inboud"
                x, y, z = self.node.getRelativePoint(self.node, self.initial_position)
                self.starting_position = (x, y, z)
                self.ending_position = self.node.getRelativePoint(self.node, dest.getPos())
                
            else:
                pass
            self.node1.setH(90)
            
            self.position3 = self.node1.posInterval(30, self.ending_position, startPos=self.starting_position)
            self.pingpong1 = Sequence(self.position3, name=self.data[4])
            self.pingpong1.loop()
            #print "This is it:" +str(self.starting_position) + ", " + str(self.ending_position)
        else:
            print "no parent found"
            
class SceneClass(template.Panda):
    def __init__(self, *args, **kwargs):
        template.Panda.__init__(self, *args, **kwargs)
        self.slugs= {}
        # Receive events
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)
        activeConnections=[]
        udpSocket = self.cManager.openUDPConnection(1723)
        self.cReader.addConnection(udpSocket)
        self.taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        self.taskMgr.add(self.update, "update")
        self.friends = dict()
        self.followers = dict()
        self._springMgr = SpringManager(self, self.render)
        self.myNode = render.attachNewNode("dummy_center_node")
        self.dummy_center_node.setPos(0, 0, 0)
        self.setBackgroundColor(0.69,0.77,0.88)
        #self.skybox = self.loader.loadModel("models/skysphere.egg")
        #self.skyboxTexture = self.loader.loadTexture("images/tron.png")
        
        #self.enableParticles()
    def objectClicked(self):
        pass
    def move(self, task):
        pass
    def update(self, task):
        self._springMgr.timer()
        return task.cont
    def buildFollowerCluster(self, lst):
        lstCount = len(lst.split(","))
        self.followerCluster = build_cluster.ModelBase(self, lstCount, 30)
        count = 0
        for l in lst.split(","):
            self.followers[ l.strip() ] = self.followerCluster.nodes[count]
            sphere = self.followerCluster.center
            self._springMgr.addSpring(sphere, self.followerCluster.nodes[count])
            count = count + 1
        print self.followers.keys()
    def buildFriendCluster(self, lst):
        lstCount = len(lst.split(","))
        self.friendCluster = build_cluster.ModelBase(self, lstCount, 15)
        count = 0
        for l in lst.split(","):
            self.friends[l.strip()] = self.friendCluster.nodes[count]
            sphere = self.friendCluster.center
            self._springMgr.addSpring(sphere, self.friendCluster.nodes[count])
            count = count + 1
        print self.friends.keys()
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                data = datagram.getMessage().split("|")
                
                if data[1] == "friendList":
                    self.buildFriendCluster( data[2] )
                elif data[1] == "followerList":
                    self.buildFollowerCluster(data[2])
                else:

                    if data[5]:
                        for d in data[5].split(","):
                            id = data[0] + data[1] + data[3] + "." + d.strip()
                            id = data[3]
                            self.moveSpring(id.replace("@", ""))

                    id = data[0] + data[1] + data[3]
                    id = data[3]
                        #self.slugs[id] = Tweet(self, id)
                    self.moveSpring(id)
                #id_builder = (data[1], data[3], data[4], data[5], data[6])
                #id = "".join(id_builder)
                #try:
                #    self.slugs[id] = slugger.Slugger(self, data, self.subnet)
                #except:
                #    raise
                
                
        return Task.cont
    def moveSpring(self, id):
        print "@%s"%id
        node2 = self.friends.get(str("@%s"%id).strip())
        if not node2:
            node2 = self.followers.get(str("@%s"%id).strip())
            node1 = self.followerCluster.center
        else:
            node1 = self.friendCluster.center
        print node1, node2
        if node2:
            node2.setColor(0.76, 0, 0, 1)
            print "moving spring"
            force = node1.getPos() - node2.getPos()
            force = Vec3( (-100/force.length()) * force.x, (-100/force.length())* force.y , (-100/force.length()) * force.z)
            self._springMgr.perturbSpring(node1, node2, force, 4000)
template.startGibson(SceneClass)