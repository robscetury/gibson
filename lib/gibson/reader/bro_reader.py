# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 08:37:53 2010

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
import re
import sys

class BroReader():
    
    def __init__(self):
        pass
    
    def format(self, record):
        out_line = ""
        addrs = []
        ports = []
        addrs = re.findall('(?:25[0-5]\.|2[0-4][0-9]\.|[01]?[0-9][0-9]?\.){3}(?:25[0-5]\.|2[0-4][0-9]\.|[01]?[0-9][0-9]?)', record)
        if len(addrs) >= 1:        
            source = addrs[0]
        else:
            source = "N/A"
        if len(addrs) == 2:
            destination = addrs[1]
        else:
            destination = "N/A"
        ports = re.findall('([0-9]+\/(?:tcp|udp))', record)
        if len(ports) >= 1:
            source_p = ports[0]
        else:
            source_p = "N/A"
        if len(ports) == 2:
            dest_p = ports[1]
        else:
            dest_p = "N/A"
        fields = record.split(" ")
        time = fields[0]
        category = fields[1]
        string = "".join(fields[2:])
        output = "|".join([time,category,"ALARM", source,source_p,destination,dest_p,string])
        
        
        return output
        
        
if __name__ == '__main__':
    reader = BroReader()
    for line in sys.stdin:
        result = reader.format(line)
        print result,
