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
import traceback
try:
    import pyximport
    pyximport.install()
    from gibson.programs.ctw3dr import *
    from gibson.programs import ctemplate as template
    print "Got the cython scene!"
except:
    traceback.print_exc()
    print "Cython not installed"
    from gibson.programs.tw3dr import *
    #from gibson.physics.pyspring import *
    from gibson.programs import template


template.startGibson(SceneClass)
print "Done with scene!"
template.scene.__del__()
print "Del called"
del(template.scene)
print "Scene deleted"