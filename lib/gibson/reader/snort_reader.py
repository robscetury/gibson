# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 11:25:36 2011

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

class SnortReader():
    
    def __init__(self):
        pass
    
    def format(self, record):
        build_array = []
        message = ""
        
        fields = record.split(" ")
        for i in fields:
            if (i == fields[0]):
                (timestamp, frac_seconds) = i.split(".") 
                timestamp = time.strptime(timestamp, "%m/%d/%y-%H:%M:%S")
                timestamp = time.mktime(timestamp)
                timestamp = str(timestamp) + "." + str(frac_seconds)
                build_array.append(timestamp)
            elif (i == fields[1] or i == fields[3] or i == fields[5]):
                continue
            elif (i == fields[2] or i == fields[4]):
                j = i.split(":")
                build_array.append(j[0])
                try:
                    if j[1] > 0:
                        if fields[5] == "TCP" or fields[5] == "UDP":
                            port = str(j[1]) + "/" + fields[5].lower()
                            build_array.append(port)
                
                except:
                    port = "0/ipv4"
                    build_array.append(port)
            else:
                message += i + " "
                
        parts = message.split('[')
    
        for i in parts:
            if i.startswith("Classification"):
                classification = i.rstrip("] ")
        output = "|" + build_array[0] + "|" + classification
        del build_array[0]
        output += "|" + "|".join(build_array)
        output += "|" + message
        output = output.rstrip()
           
            
        return output
        
        
if __name__ == '__main__':
    reader = SnortReader()
    for line in sys.stdin:
        result = reader.format(line)
        print result
