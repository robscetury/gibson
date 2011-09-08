import template
from panda3d.core import Fog
from physics import *
from pandac.PandaModules import OdeWorld

class SceneClass(template.Panda):
    def __init__(self, *args, **kwargs):
        template.Panda.__init__(self, *args, **kwargs)
        print "Hurray!"

        #self.enableParticles()
        #self.myWorld = OdeWorld()
        #self.myWorld.setGravity(0, 0, -9.81)
        self.cube = self.loader.loadModel("models/low-cube")
        self.cube.reparentTo(self.render)
        self.cube2 = self.loader.loadModel("models/low-cube")
        self.cube2.reparentTo(self.render)
        self.cube2.setPos(self.cube, 10,20,30)
        self.cube2.setHpr(175,3,45)
        self.spring = Spring(self, self.render,  self.cube, self.cube2)
        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.move, "move")
        self._dir = 1

        colour = (0.5,0.8,0.8)
        linfog = Fog("A linear-mode Fog node")
        linfog.setColor(*colour)
        linfog.setLinearRange(0,320)
        linfog.setLinearFallback(45,160,320)
        render.attachNewNode(linfog)
        render.setFog(linfog)
        #self.cube2.setPos(self.cube, 15, 5, 5)
        self.spring.perturb(Vec3(25,25,1))
    def objectClicked(self):
        #self.cube2.setPos(self.cube, 15, 5, 5)
        self.spring.perturb( Vec3(10,10,10), 2500)
    def move(self, task):
        
        #r = self.cube.getHpr()
        #r.addX(5)
        #r.addY(1)
        #r.addZ(-10)
        #self.cube.setHpr(r)
        return task.again
    def update(self, task):
       
       #r = self.cube2.getHpr()
       ##r.addX(1)
       #r.addY(1)
       #r.addZ(-1)
       #self.cube2.setHpr(r)
       self.spring.timer()
       return task.again
template.startGibson(SceneClass)
