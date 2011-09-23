try:
    import pyximport
    pyximport.install()
    from gibson.physics.spring import * 
    print "Got the cython spring!"
except:
    print "Cython not installed"
    from gibson.physics.pyspring import *


