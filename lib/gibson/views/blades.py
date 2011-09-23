# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 16:53:16 2011

@author: -
"""
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
# Making blades

from gibson import getPath

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
            self.servers.append(panda.loader.loadModel(getPath("model", "crt.egg")))
            self.servers[num].reparentTo(self.blades[blade_num])
            y = ((num % 16) % 4) * 10
            z = (int((num % 16)/4)) * 10
            self.servers[num].setPos(0, y, z)
            
            