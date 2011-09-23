# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 17:45:09 2011

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
import sys
import time
import socket

class SyslogReader():
    
    def __init__(self):
        pass
    
    def format(self, record):
        out_line = ""
        fields = record.split(" ")
        dt = time.localtime()
        year = dt[0]
        timestamp = fields[0] + " " + str(fields[2]) + " " + str(year) + " " + fields[3]
        timestamp = time.strptime(timestamp, "%b  %d %Y %H:%M:%S")
        timestamp = time.mktime(timestamp)
        output = "|" + str(timestamp)
        output += "|" + fields[8].rstrip("]") + "|"
        try:
            ip = socket.gethostbyname(fields[4])
        except socket.gaierror:
            ip = fields[4]
        output += ip
        output += '|N/A|N/A|N/A|'
        output += " ".join(fields[5:])
        return output
        
        
if __name__ == '__main__':
    reader = SyslogReader()
    for line in sys.stdin:
        result = reader.format(line)
        print result,
