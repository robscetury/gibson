# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:18:05 2010

@author: -
"""

from gibson.reader import send_event
from gibson.reader import bro_reader
from gibson.reader import snort_reader
from gibson.reader import syslog_reader
from  gibson.twitter import twitter_reader
import sys

if len(sys.argv)>=4:
    host = sys.argv[1]  
    port = int(sys.argv[2])
    if sys.argv[3] == "bro":
        reader = bro_reader.BroReader()
    elif sys.argv[3] == "snort":
        reader = snort_reader.SnortReader()
    elif sys.argv[3] == "syslog":
        reader = syslog_reader.SyslogReader()
    elif sys.argv[3] == 'twitter':
        reader = twitter_reader.TwitterReader(host, port)
        reader.run()
    if reader:
        socket = send_event.EncapsulateForPanda()
        for line in sys.stdin:
            message = reader.format(line)
            socket.send_event(host, port, message)
    else:
            reader.run()
print "Usage: event_daemon.py IP port [bro|snort|syslog|twitter]"

