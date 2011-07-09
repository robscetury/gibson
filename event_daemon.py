# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:18:05 2010

@author: -
"""

import send_event
import bro_reader
import snort_reader
import syslog_reader

import sys

host = sys.argv[1]
port = int(sys.argv[2])
if sys.argv[3] == "bro":
    reader = bro_reader.BroReader()
elif sys.argv[3] == "snort":
    reader = snort_reader.SnortReader()
elif sys.argv[3] == "syslog":
    reader = syslog_reader.SyslogReader()
else:
    print "Usage: event_daemon.py IP port [bro|snort|syslog]"
socket = send_event.EncapsulateForPanda()
for line in sys.stdin:
    message = reader.format(line)
    socket.send_event(host, port, message)
