# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 19:42:02 2010

@author: -
"""

import random
notices = []
addresses = []
f = open('notices_from_bro', 'r')
for i in f:
    notices.append(i)
    
g = open('addresses', 'r')
for j in g:
    addresses.append(j)
    

for a in range(1000):
    time = random.uniform(1280000000.000000, 1293673450.000000)
    notice = random.choice(notices)
    ip = random.choice(addresses)
    print "t=" + str(time) + " no=" + notice[:-1] + " na=NOTICE_ALARM_ALWAYS sa=" + ip[:-1] + " sp=60127/tcp da=79.120.86.20 dp=12444/tcp msg=We\\ have\\ a\\ problem tag=@5f-723-2e3d"
