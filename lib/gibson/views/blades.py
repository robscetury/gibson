# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 16:53:16 2011

@author: -
"""

# Making blades

class BladeView():
    def __init__(self, panda):
        self.blades = []
        self.servers = []
        number_of_blades = len(panda.model.servers) % 16
        for blade_num in range(number_of_blades):
            self.blades.append(panda.NodePath(blade_num))
            self.blades[blade_num].show()
            self.blades[blade_num].reparentTo(render)
            self.blades[blade_num].setPos(blade_num*15, 0, 0)
            self.blades[blade_num].setTag('state', 'in')
            
        for server in panda.model.servers:
            num = panda.model.servers.index(server)
            blade_num = int((num / 16) +1)
            self.servers.append(panda.loader.loadModel("crt.egg"))
            self.servers[num].reparentTo(self.blades[blade_num])
            y = ((num % 16) % 4) * 10
            z = (int((num % 16)/4)) * 10
            self.servers[num].setPos(0, y, z)
            
            