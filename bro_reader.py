# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 08:37:53 2010

@author: -
"""

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
        
        #new_line = record.replace("\\ ", "\\")
        #fields = new_line.split(" ")
        #for i in fields:
        #    if (i == fields[2]):
        #        continue
        #    parts = i.split("=")
        #    dumb_array = (out_line, parts[1])
        #    out_line = "|".join(dumb_array)
        #output = out_line.replace("\\"," ")
        return output
        
        
if __name__ == '__main__':
    reader = BroReader()
    for line in sys.stdin:
        result = reader.format(line)
        print result,
