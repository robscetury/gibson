from pandac.PandaModules import OdeBody, OdeMass, ActorNode, Vec3, ForceNode, LinearVectorForce, NodePath

class Spring(object):

      def __init__(self, base, render,  node1, node2, nodeMass=1, springConstant = 1, drag=5):
            self._render = render
            self._base = base
            self._base.enableParticles()
            self._node1 = node1
            self._node2 = node2
            self._actor1 = ActorNode()
            node1 = NodePath("PhysicsNode1")
            node1.reparentTo(render)
            anp1 = node1.attachNewNode(self._actor1)
            base.physicsMgr.attachPhysicalNode(self._actor1)
            self._actor1.getPhysicsObject().setMass(nodeMass)
            self._node1.reparentTo(anp1)
            node2 = NodePath("PhysicsNode2")
            node2.reparentTo(render)
            self._actor2 = ActorNode()
            anp2 = node2.attachNewNode(self._actor2)
            base.physicsMgr.attachPhysicalNode(self._actor2)
            self._actor2.getPhysicsObject().setMass(nodeMass)
            self._node2.reparentTo(anp2) 
            self._springConstant = float(springConstant)
            self._drag = float(drag)
            self.lastTime = globalClock.getDt()
            self._zeroDistance = self._node1.getPos() - self._node2.getPos()
            self._force1 = None
            self._force2 = None
            self._lastPosNode1 = self._node1.getPos()
            self._lastPosNode2 = self._node2.getPos()
            self._impulse1 = None
            self._impulse2 = None
            self._timeOut = None
      def timer(self):
            actor1 = self._actor1.getPhysical(0)
            actor2 = self._actor2.getPhysical(0)
            if self._force1:
                  actor1.removeLinearForce(self._force1)
                  actor2.removeLinearForce(self._force2)
            if self._impulse1:
                  if globalClock.getLongTime() > self._timeOut:
                        print "removing perturbation"
                        try:
                              actor1.removeLinearForce(self._impulse1)
                              actor2.removeLinearForce(self._impulse2)
                        except Exception, e:
                              print e
                              print "failed"
                        self._impulse1 = None
                        self._impulse2 = None
                        self._timeOut = None
            force = self.getForce()
            #print force
            
            
            
            if force:
                  forceVector = self._node1.getPos() - self._node2.getPos()
                  self._force1 = ForceNode('force1')
                  self._node1.attachNewNode(self._force1)
                  force2 = self._node2.getRelativeVector( self._node1, force)
                  lvf1 = LinearVectorForce(force.x , force.y, force.z)
                  #print force
                  self._force1.addForce( lvf1 )
                  lvf1.setMassDependent(1)
                  self._force2 = ForceNode('force2')
                  self._node2.attachNewNode(self._force2)
                  lvf2 = LinearVectorForce( LinearVectorForce( Vec3( -1* force2.x, -1 * force2.y, -1* force2.z)))
                  lvf2.setMassDependent(1)
                  self._force2.addForce(lvf2)
                  #self._base.physicsMgr.addLinearForce(lvf1)
                  #self._base.physicsMgr.addLinearForce(lvf2)
                  self._actor1.getPhysical(0).addLinearForce(lvf1)
                  self._actor2.getPhysical(0).addLinearForce(lvf2)
                  self._force1 = lvf1
                  self._force2 = lvf2

      def getForce(self):
            
            #newTime = globalClock.getDt()
            #if newTime > self.lastTime:
            distance = self._node1.getPos(self._render) - self._node2.getPos(self._render)
            #print 'distance %s'%distance
            zDistance = self._zeroDistance
            force = Vec3( self._springConstant * ( zDistance.x - distance.x), self._springConstant * (zDistance.y - distance.y), self._springConstant* (zDistance.z - distance.z))
                          
                          
                          
            posDelta1 = self._node1.getPos(self._render) - self._lastPosNode1
            
            posDelta2 =  self._node2.getPos(self._render) - self._lastPosNode2
            #print posDelta1, posDelta2
            posDelta = posDelta1 + posDelta2
            self._lastPosNode1 = self._node1.getPos(self._render)
            self._lastPosNode2 = self._node2.getPos(self._render)
            posVec = self._node1.getPos(self._render) - self._node2.getPos(self._render)
            
            #print force
            clock = globalClock.getDt()
            velocity = self._actor1.getPhysicsObject().getVelocity()
            force2Vec = Vec3( velocity.x  * (  self._drag), velocity.y  * ( self._drag),  velocity.z*(self._drag))
            
            #print "Drag Force " + str(force2Vec)
            force = self._roundVec(force - force2Vec)
            #print "Spring force " + str(force)
            #self.lastTime = newTime
            #print "Combined " + str(force)
            if force.length()>.01:
                  return force      
      
                                                                    
      def round_to_n(self, x, n):
            if n < 1:
                  raise ValueError("number of significant digits must be >=1")
            format = "%." + str(n-1) + "e"
            as_string = format % x
            return round(float(as_string), n)
      def _roundVec(self,vector):

            vector.x = self.round_to_n(vector.x, 3)
            vector.y = self.round_to_n(vector.y, 3)
            vector.z = self.round_to_n(vector.z, 3)
            return vector

      def perturb(self, force, time=1000):
            print "perturbing %s, %s"%(force, time)
            node1 = self._node1
            node2 = self._node2
            actor1 = self._actor1
            actor2 = self._actor2
            self._timeOut = globalClock.getLongTime() + time/1000
            force2 = node2.getRelativeVector( node1, force)
            force2 = Vec3( -1*force2.x, -1*force2.y, -1*force2.z)
            
            forceN1 = ForceNode('Impulse1')
            lvf1 = LinearVectorForce( force )
            lvf1.setMassDependent(1)
            forceN1.addForce(lvf1)
            node1.attachNewNode(forceN1)
            actor1.getPhysical(0).addLinearForce(lvf1)
            forceN2 = ForceNode("Impulse2")
            lvf2 = LinearVectorForce( force2)
            lvf2.setMassDependent(1)
            forceN2.addForce(lvf2)
            node2.attachNewNode(forceN2)
            actor2.getPhysical(0).addLinearForce(lvf2)
            self._impulse1 = lvf1
            self._impulse2 = lvf2