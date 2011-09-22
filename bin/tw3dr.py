
from gibson.programs import template
from gibson.programs.tw3dr import *

template.startGibson(SceneClass)
print "Done with scene!"
template.scene.__del__()
print "Del called"
del(template.scene)
print "Scene deleted"