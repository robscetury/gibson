# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:18:05 2010

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
        print "Usage: event_daemon.py IP port [bro|snort|syslog|twitter]"

