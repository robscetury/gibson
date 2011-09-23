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
__author__ = 'rob'
import traceback

from gibson import template
from panda3d.core import Fog
from gibson.physics import *
from pandac.PandaModules import *
from direct.task import Task
from gibson.views import build_cluster
from gibson.slugs import *
import random
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from gibson.ui import keyboard_events
from gibson.ui import gui

import netaddr
import subprocess
from math import pi, atan
import time
import random
import re
import traceback
import os
from gibson import *
FOAF_FORCE = Vec3(1,1,1)
FOAF_SPRING_CONST=1
FRIEND_SPRING_CONST=5
FOAF_DRAG=5
FRIEND_DRAG=15

TWEET_FORCE=-10
TWEET_FORCE_TIME=2000

class Tw3drKeyboardEvents(keyboard_events.KeyboardEvents):
    def __init__(self, camera, panda):
        keyboard_events.KeyboardEvents.__init(self, camera, panda)
        self.accept('p', self.PostUpdate)
        self.accept('[', self.DirectMessage)

    def PostEvent(self):
        pass

class Tweet(SluggerBase):
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
            self.dest =dest
            parent.setTag("Status", self.data[-1])
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
            self.node1 = self.panda.loader.loadModel(getPath("model","slug2.egg"))
            self.node1.reparentTo(dest)
            self.node1.setPos( dest.getRelativePoint(dest, parent.getPos()))
            self.node1.lookAt(dest)
            self.node1.setTag('postedby', self.data[3])
            self.node1.setTag('myObjectTag', self.data[-1])
            if len(self.data[5].split( ","))> 0:
                self.node1.setTag("Mentions", self.data[5])
            #self.node1.setH(90)
            self.node1.setHpr(dest, Vec3(90, 90,180))
            self.position3 = self.node1.posInterval(30, self.ending_position, startPos=self.starting_position)
            self.pingpong1 = Sequence(self.position3)#, name=self.data[-1])
            self.pingpong1.start()
            return


            #print parent
            self.node = self.panda.loader.loadModel(getPath("model", "slug2.egg"))
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
            self.node1 = self.panda.loader.loadModel(getPath("model", "slug2.egg"))
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
        skybox_model = getPath("model", "skysphere.egg")
        try:

            self.skybox = self.loader.loadModel(skybox_model)

        except:
            traceback.print_exc()
            print "Skybox Model not found"
        texture=getPath("image", "book.jpg")

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
        self.center = self.loader.loadModel(getPath("model", "crt.egg"))
        self.center.reparentTo(self.render)
        self.center.setColorScale(0.7, 0.41, 0.80, 1)
        #self.center.setScale(2)
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
        self._tempFiles = list()
        self.MyUserId = None
        self.view = ""


    def buildOortCloud(self, username, foafList):

        print "in buildOortCloud"
        foaflist = foafList.split(",")
        for u in foaflist:
            #print u
            if u in self.followers:# and not u == self.MyUserId:
                print "gotta follower %s"%u
                node = self.followers[u]
                sphere = self.center
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
                    s= self._springMgr.addSpring( self.followers[username], node, springConstant=FOAF_SPRING_CONST,drag=FOAF_DRAG)
                    zDistance = s._zeroDistance
                    #s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    print s._zeroDistance
                elif username in self.friends:
                    s= self._springMgr.addSpring( self.friends[username], node, springConstant=FOAF_SPRING_CONST,drag=FOAF_DRAG)
                    zDistance = s._zeroDistance
                    #s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    print s._zeroDistance
                if s:
                    s.perturb(FOAF_FORCE, 1500)
            elif u in self.friends:# and not u == self.MyUserId:
                node = self.friends[u]
                sphere = self.center
                s = self._springMgr._springMap.get( (sphere, node) )
                if s:
                    #print s._zeroDistance
                    zDistance = s._zeroDistance
                    #s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    #print s._zeroDistance
                    newZDistance = s._zeroDistance
                    #s = self._springMgr.addSpring(sphere, node, lengthFactor =3)
                        #newZDistance = s._zeroDistance
                    #print newZDistance
                    #node.setPos( newZDistance.x, newZDistance.y, newZDistance.z)
                    s.perturb(FOAF_FORCE, 1500)
                if username in self.friends:
                    s = self._springMgr.addSpring( self.friends[username], node,springConstant=FOAF_SPRING_CONST, drag=FOAF_DRAG)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    #s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                    s.perturb(FOAF_FORCE, 1500)
                elif username in self.followers:
                    s = self._springMgr.addSpring( self.followers[username], node,springConstant=FOAF_SPRING_CONST, drag=FOAF_DRAG)
                    zDistance = s._zeroDistance
                    s._zeroDistance = Vec3( zDistance.x/2, zDistance.y/2, zDistance.z/2 )
                    #s._zeroDistance = Vec3( (zDistance.x/zDistance.length()) *20, (zDistance.y/zDistance.length()) * 20 , (zDistance.z/zDistance.length()) * 20 )
                    print s._zeroDistance
                    s.perturb(FOAF_FORCE, 1500)
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
        for f in self._tempFiles:
            try:
                os.remove(f)
            except:
                pass
    #def objectClicked(self):
    #    pass
    def move(self, task):
        pass
    def update(self, task):
        #self._springMgr.timer()
        delList = list()
        for slug in self.slugs:
            if hasattr(self.slugs[slug], "node1"):

                if self.slugs[slug].node1.getPos(self.slugs[slug].dest) <= 1 :
                    print "deleting slug"
                    delList.append( slug)
                    #del self.slugs[slug]
            else:
                delList.append(self.slugs[slug])
                #del self.slugs[slug]
                #slug.pingpong1.getState()
        for s in delList:
            try:
                del self.slugs[slug]
            except:
                pass
        return task.cont
    def buildFollowerCluster(self, lst):
        lst = lst.replace(self.MyUserId + ",", "")
        lstCount = len(lst.split(","))
        self.followerCluster = build_cluster.ModelBase(self, lstCount,75, center=self.center, scale = 1)
        count = 0
        for l in lst.split(","):
            if l.strip() not in self.friends:
                self.followers[ l.strip() ] = self.followerCluster.nodes[count]
                self.followers[ l.strip()].setColor(.8, .8, .8, .5)
                self.followers[l.strip()].setTag("myObjectTag", "follower|%s"%l.strip())
                sphere = self.followerCluster.center
                self._springMgr.addSpring(sphere, self.followerCluster.nodes[count],springConstant=FRIEND_SPRING_CONST, drag=FRIEND_DRAG)
                count = count + 1
        #print self.followers.keys()
    def buildFriendCluster(self, lst):
        lst = lst.replace(self.MyUserId + ",", "")
        lstCount = len(lst.split(","))
        self.friendCluster = build_cluster.ModelBase(self, lstCount, 50, center=self.center, scale = 1)
        count = 0
        for l in lst.split(","):
            if l.strip() not in self.followers:
                self.friends[l.strip()] = self.friendCluster.nodes[count]
                self.friends[l.strip()].setColor(.5,.5,5,.3)
                self.friends[l.strip()].setTag("myObjectTag", "friend|%s"%l.strip())
                sphere = self.friendCluster.center
                self._springMgr.addSpring(sphere, self.friendCluster.nodes[count], springConstant=FRIEND_SPRING_CONST, drag=FRIEND_DRAG)
                count = count + 1
        #print self.friends.keys()
    def tskReaderPolling(self,taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()
            if self.cReader.getData(datagram):
                data = datagram.getMessage().split("|")
                print data
                if data[1] == "Me":
                    #print data
                    self.MyUserId = "@%s"%data[2].strip()
                    self.center.setTag("myObjectTag", "Me|@%s"%data[2].strip())
                    self.center.setTag("Status", data[3])
                    self.friends["@%s"%data[2]] = self.center
                elif data[1] == "friendList":
                    self.buildFriendCluster( data[2] )
                elif data[1] == "followerList":
                    self.buildFollowerCluster(data[2])
                elif data[1] == "foaf":
                    self.buildOortCloud(data[2], data[3])
                elif data[1] == "textureFile":
                    self.applyTexture(data[2], data[3])
                elif data[1] == "InitStatus":
                    fr = self.friends.get("@%s"%data[2])
                    if not fr:
                        fr = self.followers.get("@%s"%data[2])
                    if fr:
                        fr.setTag("Status", data[3])


                elif data[1] == "Status" or data[1]=="Mention":

                    if data[5]:
                        for d in data[5].split(","):
                            id = data[0] + data[1] + data[3] + "." + d.strip()
                            id = data[3]

                            try:
                                self.moveSpring(id.replace("@", ""))
                                self.slugs["|".join(data)] = Tweet(self, data)
                            except:
                                pass

                    id = data[0] + data[1] + data[3]
                    id = data[3]
                    try:
                        self.slugs["|".join(data)] = Tweet(self, data)
                        self.moveSpring(id)
                    except:
                        pass

                else:
                    print data[1] + "not found"

                #id_builder = (data[1], data[3], data[4], data[5], data[6])
                #id = "".join(id_builder)
                #try:
                #    self.slugs[id] = slugger.Slugger(self, data, self.subnet)
                #except:
                #    raise


        return Task.cont
    def applyTexture(self, name, filename):
        self._tempFiles.append(filename)
        try:
            t = self.loader.loadTexture(filename)
            t.setWrapU(Texture.WMMirror)
            t.setWrapV(Texture.WMMirror)
            if name == self.center.getTag("myObjectTag"):
                node = self.center
            else:
                node = self.followers.get("@%s"%name)
            if not node:
                node = self.friends.get("@%s"%name)
            if node:
                node.clearTexture()
                node.setColorOff()
                node.setColorScaleOff()
                #node.setColor(1,1,1,1)
                #node.clearColor()
                node.setTexture(t)

        except:
            print name
            traceback.print_exc()

    def moveSpring(self, id):

        node2 = self.friends.get(str("@%s"%id).strip())
        if not node2:
            node2 = self.followers.get(str("@%s"%id).strip())
            node1 = self.followerCluster.center
        else:
            node1 = self.friendCluster.center

        if node2:
            #node2.setColor(0.76, 0, 0, 1)
            print "moving spring"
            force = node1.getPos() - node2.getPos()
            force = Vec3( (TWEET_FORCE/force.length()) * force.x, (TWEET_FORCE/force.length())* force.y , (TWEET_FORCE/force.length()) * force.z)
            self._springMgr.perturbSpring(node1, node2, force, TWEET_FORCE_TIME)

    def findFriend(self, friendNode, friendId):
        self.UserPopup(friendNode, friendId)
    def findFollower(self, followerNode, follower):
        self.UserPopup(followerNode, follower)
    def findMe(self, centerNode, me):
        self.UserPopup(centerNode, me)
    def UserPopup(self, node, fId):
        fId = fId.split("|")[-1]
        info = TextNode(str(fId))
        text = "\n".join( [fId, node.getTag("Status")])
        #text = "\n".join(i.data[1:])
        info.clearTextColor()
        info.clearCardTexture()

        info.setText(text)
        info.setCardAsMargin(0, 0, 0.5, 0)
        info.setCardColor(1.0, 1.0, 1.0, 0.7)
        info.setTextColor(1.0, 0.0, 0.0, 1.0)
        info.setFrameAsMargin(0, 0, 0.5, 0)
        info.setFrameColor(0.0, 0.0, 0.0, .9)
        info.setCardDecal(True)
        clickable = info.generate()
        self.popup = node.attachNewNode(clickable)
        self.popup.reparentTo(node)
        self.popup.setH(270)
        #self.popup.setScale(0.25)
        x, y, z = node.getPos()
        #self.popup.setPos(-3, 3, 3)
        self.popup.setTag('myObjectTag', 'ServerPopUp')
        self.popup.setLightOff()
        self.popup.setTexture(Texture())
        #self.popup.setTextureOff(1)
        #self.popup.setScale(0.10)
        #self.popup.setPos(-3, 0, 3)

        #self.popup.setH(self.camera, 150)
        self.popup.lookAt(self.camera)
        #self.popup.setCompass(self.camera)
        self.popup.setHpr(self.camera, 0, 0, 0)
    def objectClicked(self):

        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

        self.myTraverser.traverse(render)
        # Assume for simplicity's sake that myHandler is a CollisionHandlerQueue.
        #print self.myHandler.getNumEntries()
        if self.myHandler.getNumEntries() > 0:
            for i in range(self.myHandler.getNumEntries()):
                entry = self.myHandler.getEntry(i)
                #print entry
            self.myHandler.sortEntries()
            pickedObj = self.myHandler.getEntry(0).getIntoNodePath()

            obj_id = pickedObj.getNetTag('myObjectTag')


            #try:
            #    pickedObj2 = self.myHandler.getEntry(1).getIntoNodePath()
            #    obj_id2 = pickedObj2.getNetTag('myObjectTag')
            #    print obj_id2
            #except:
            #    traceback.print_exc()
            #    pass
            #
            #try:
            #    pickedObj3 = self.myHandler.getEntry(2).getIntoNodePath()
            #    obj_id3 = pickedObj3.getNetTag('myObjectTag')
            #    print obj_id3
            #except:
            #    traceback.print_exc()
            #    pass

            pickedObj = pickedObj.findNetTag('myObjectTag')
            if not pickedObj.isEmpty():
                if obj_id.startswith("friend"):
                    self.findFriend(pickedObj, obj_id)
                elif obj_id.startswith("follower"):
                    self.findFollower(pickedObj, obj_id)
                elif obj_id.startswith("Me"):
                    self.findMe(pickedObj, obj_id)

                elif obj_id == "PopUp":

                    if pickedObj.getAncestor(1).getNetTag("type") == "Tunnel":
                        pickedObj.removeNode()
                    else:
                        #pickedObj.getAncestor(1).setScale(2)
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


        info = TextNode(str(slug_id))
        text = "\n".join( [slug.getTag("postedby"), slug.getTag("Mentions"), slug_id])
        #text = "\n".join(i.data[1:])
        info.clearTextColor()
        info.setText(text)
        info.setCardAsMargin(0, 0, 0.5, 0)
        info.setCardColor(1.0, 1.0, 1.0, 0.7)
        info.setTextColor(1.0, 0.0, 0.0, 1.0)
        info.setFrameAsMargin(0, 0, 0.5, 0)
        info.setFrameColor(0.0, 0.0, 0.0, .9)
        info.setCardDecal(True)
        clickable = info.generate()
        self.popup = slug.attachNewNode(clickable)
        info.clearCardTexture()
        self.popup.reparentTo(slug)
        self.popup.setH(270)
        self.popup.setTexture(Texture())
        #self.popup.setScale(0.25)
        x, y, z = slug.getPos()
        #self.popup.setPos(-3, 3, 3)
        self.popup.setTag('myObjectTag', 'PopUp')
        #self.popup.setTextureOff()
        self.popup.setLightOff()

        #self.popup.setScale(0.10)
        #self.popup.setPos(-3, 0, 3)

        #self.popup.setH(self.camera, 150)
        self.popup.lookAt(self.camera)
        #self.popup.setCompass(self.camera)
        self.popup.setHpr(self.camera, 0, 0, 0)


        #i.node.setScale(1.25)


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

        info.setText(text)
        info.setCardAsMargin(0, 0, 0.5, 0)
        info.setCardColor(1.0, 1.0, 1.0, 0.7)
        info.setTextColor(0.0, 0.0, 0.0, 1.0)
        info.setFrameAsMargin(0, 0, 0.5, 0)
        info.setFrameColor(0.0, 0.0, 0.0, .9)
        info.setCardDecal(True)
        clickable = info.generate()
        self.popup = self.attachNewNode(clickable)
        self.popup.reparentTo(server)
        #self.popup.setH(270)
        #self.popup.setScale(0.5)
        self.popup.setPos(-3, -5, 0)
        self.popup.clearTexture()
        self.popup.setTag('myObjectTag', 'ServerPopUp')
        self.popup.setLightOff()
