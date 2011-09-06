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
import subprocess
from math import pi, atan
import time
import random
import re

FOAF_FORCE = Vec3(50,50,50)

class Tweet(slugger.SluggerBase):
    def __init__(self,panda, data):
        slugger.SluggerBase.__init__(self, panda, data)
        #self.dest = dest
        self.createSlug("Inbound")
        
    def createSlug(self, direction):
        #print u"creating slug for @%s"%self.data[3]
        parentName = str("@%s"%self.data[3])
        parent = self.panda.friends.get(parentName.strip())
        #dest = self.panda.dummy_center_node
        #dest = self.dest
        if not parent:
            parent = self.panda.followers.get(parentName.strip())
            dest = self.panda.followerCluster.center
        else:
            dest = self.panda.friendCluster.center
        if parent:
            self.starting_position = dest.getRelativePoint(dest, parent.getPos())
            print "found Parent"
            #self.node = self.panda.loader.loadModel('models/slug2.egg')
            #self.node.setPos(parent.getPos())
            self.initial_position = dest.getRelativePoint(dest, parent.getPos())
            print self.initial_position
            self.ending_position = dest.getRelativePoint(dest, dest.getPos())
            print self.ending_position
            #self.position1 = self.node.posInterval(30, self.ending_position, startPos=self.starting_position, fluid=1)
            #self.position2 = self.node.posInterval(30, self.starting_position, startPos=self.ending_position, fluid=1)
            #self.pingpong = Sequence(self.position1, self.position2, name=self.data[-1])
            #self.pingpong.start()
            self.node1 = self.panda.loader.loadModel("models/slug2.egg")
            self.node1.reparentTo(dest)
            self.node1.setPos( dest.getRelativePoint(dest, parent.getPos()))
            self.node1.lookAt(dest)
            #self.node1.setH(90)
            self.node1.setHpr(dest, Vec3(90, 90,180))
            self.position3 = self.node1.posInterval(30, self.ending_position, startPos=self.starting_position)
            self.pingpong1 = Sequence(self.position3)#, name=self.data[-1])
            self.pingpong1.start()
            return
        
        
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
        self.taskMgr.doMethodLater(2, self.startEventDaemon, 'launch')
        self.friends = dict()
        self.followers = dict()
        self._springMgr = SpringManager(self, self.render)
        self.myNode = render.attachNewNode("dummy_center_node")
        self.dummy_center_node.setPos(0, 0, 0)
        print "Setting up skybox"
        self.camera.reparentTo(self.dummy_center_node)
        bg_color = (0.69,0.77,0.88)
        #self.setBackgroundColor(bg_color)
        skybox_model = "models/skysphere.egg"
        try:

            self.skybox = self.loader.loadModel(skybox_model)
               
        except:
            traceback.print_exc()
            print "Skybox Model not found"
        texture="images/book.jpg"
        try:
            self.skyboxTexture = self.loader.loadTexture(texture)
        except:
            print "Skybox texture not found."
        print self.skybox, self.skyboxTexture
        #self.skyboxTexture.setWrapU(Texture.WMRepeat)     
        #self.skyboxTexture.setWrapV(Texture.WMRepeat)        

        
    
        self.skybox.reparentTo(self.cam)
        self.skybox.setScale(2)
        self.skybox.setCompass()
        self.camLens.setFar(500)
        self.skybox.setTexture(self.skyboxTexture, 1)
        self.skybox.setBin('background', 1)
        self.skybox.setDepthWrite(0)
        self.skybox.setLightOff()
          
        self.skybox.setCollideMask(BitMask32.allOff())
        print "done"
        #self.setBackgroundColor(0.69,0.77,0.88)
        self.finalExitCallbacks.append(self.cleanup)
        self._oortCloudDistance = 501
        self._oortCloudClusters = dict()
        self._oortCloudNodes = dict()
        self.center = self.loader.loadModel("models/sphere.egg")
        self.center.reparentTo(self.render)
        self.center.setColorScale(0.7, 0.41, 0.80, 1)
        
    def buildOortCloud(self, username, foafList):
        print "in buildOortCloud"
        foaflist = foafList.split(",")
        for u in foaflist:
            #print u
            if u in self.followers:
                print "gotta follower %s"%u 
                node = self.followers[u]
                sphere = self.followerCluster.center
                s = self._springMgr._springMap[ (sphere, node)]
                #print s._zeroDistance
                #zDistance = s._zeroDistance
                #s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                #print s._zeroDistance
                newZDistance = s._zeroDistance
                #node.setPos( newZDistance.x, newZDistance.y, newZDistance.z)
                s.perturb(FOAF_FORCE)
                s = None
                if username in self.followers:
                    s= self._springMgr.addSpring( self.followers[username], node)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                elif username in self.friends:
                    s= self._springMgr.addSpring( self.friends[username], node)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                if s:
                    s.perturb(FOAF_FORCE, 2000)
            elif u in self.friends:
                node = self.friends[u]
                sphere = self.friendCluster.center
                s = self._springMgr._springMap[ (sphere, node)]
                #print s._zeroDistance
                #zDistance = s._zeroDistance
                #s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                #print s._zeroDistance
                #newZDistance = s._zeroDistance
                #s = self._springMgr.addSpring(sphere, node, lengthFactor =3)
                #newZDistance = s._zeroDistance
                #print newZDistance
                #node.setPos( newZDistance.x, newZDistance.y, newZDistance.z)
                s.perturb(FOAF_FORCE, 2000)
                if username in self.friends:
                    s = self._springMgr.addSpring( self.friends[username], node)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                    s.perturb(FOAF_FORCE, 2000)
                elif username in self.followers:
                    self._springMgr.addSpring( self.followers[username], node)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                    s.perturb(FOAF_FORCE, 2000)
                print "gotta friend %s"%u
            else:
                #return # for now, see if it is causing performance issues to have all these nodes and springs
                #lstCount = len(foafList.split(","))
                #self._oortCloudClusters[username]=build_cluster.ModelBase(self, lstCount, self._oortCloudDistance, center=self.center)
                
                
                #self._oortCloudDistance += 10
                #count = 0
                #for l in foafList.split(","):
                #    if l.strip() not in self._oortCloudNodes:
                #        self._oortCloudNodes[ l.strip() ] = self._oortCloudClusters[username].nodes[count]
                #        self._oortCloudNodes[ l.strip()].setColor(.4, .4, .4, .5)
                #        sphere = self._oortCloudClusters[username].center
                #        self._springMgr.addSpring(sphere, self._oortCloudClusters[username].nodes[count])
                #        count = count + 1
                #print "put in Oort Cloud"
                pass
    def startEventDaemon(self, task):
        self._daemon = subprocess.Popen(['ppython',
                                         'event_daemon.py',
                                         'localhost',
                                         '1723',
                                         'twitter'])
        return task.done
    
    def cleanup(self):
        print "gc called"
        if hasattr(self, "_daemon"):
            print "killing"
            #self._daemon.kill()
            #self._daemon.kill()
            pid = self._daemon.pid
            subprocess.call(["kill", "-9", str(pid)])
            self._daemon = None
            print "killed"
    def objectClicked(self):
        pass
    def move(self, task):
        pass
    def update(self, task):
        #self._springMgr.timer()
        delList = list()
        for slug in self.slugs:
            if hasattr(self.slugs[slug], "node1"):
                if self.slugs[slug].node1.getPos() == Vec3(0,0,0):
                    print "deleting slug"
                    delList.append( slug)
                    #del self.slugs[slug]
            else:
                #del self.slugs[slug]
                delList.append(slug)
        for s in delList:
            del self.slugs[s]
        return task.cont
    def buildFollowerCluster(self, lst):
        lstCount = len(lst.split(","))
        self.followerCluster = build_cluster.ModelBase(self, lstCount,75, center=self.center)
        count = 0
        for l in lst.split(","):
            if l.strip() not in self.friends:
                self.followers[ l.strip() ] = self.followerCluster.nodes[count]
                self.followers[ l.strip()].setColor(.8, .8, .8, .5)
                sphere = self.followerCluster.center
                self._springMgr.addSpring(sphere, self.followerCluster.nodes[count])
                count = count + 1
        #print self.followers.keys()
    def buildFriendCluster(self, lst):
        lstCount = len(lst.split(","))
        self.friendCluster = build_cluster.ModelBase(self, lstCount, 50, center=self.center)
        count = 0
        for l in lst.split(","):
            if l.strip() not in self.followers:
                self.friends[l.strip()] = self.friendCluster.nodes[count]
                self.friends[l.strip()].setColor(.5,.5,5,.3)
                sphere = self.friendCluster.center
                self._springMgr.addSpring(sphere, self.friendCluster.nodes[count])
                count = count + 1
        #print self.friends.keys()
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                data = datagram.getMessage().split("|")
                
                if data[1] == "friendList":
                    self.buildFriendCluster( data[2] )
                elif data[1] == "followerList":
                    self.buildFollowerCluster(data[2])
                elif data[1] == "foaf":
                    self.buildOortCloud(data[2], data[3])
                else:

                    if data[5]:
                        for d in data[5].split(","):
                            id = data[0] + data[1] + data[3] + "." + d.strip()
                            id = data[3]
                            self.moveSpring(id.replace("@", ""))
                            self.slugs["|".join(data)] = Tweet(self, data)

                    id = data[0] + data[1] + data[3]
                    id = data[3]
                    
                    self.slugs["|".join(data)] = Tweet(self, data)
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
            #node2.setColor(0.76, 0, 0, 1)
            print "moving spring"
            force = node1.getPos() - node2.getPos()
            force = Vec3( (-100/force.length()) * force.x, (-100/force.length())* force.y , (-100/force.length()) * force.z)
            self._springMgr.perturbSpring(node1, node2, force, 4000)

template.startGibson(SceneClass)
print "Done with scene!"
template.scene.__del__()
print "Del called"
del(template.scene)
print "Scene deleted"