# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 08:37:53 2010

@author: -
"""

import sys

class BroReader():
    
    def __init__(self):
        pass
    
    def format(self, record):
        out_line = ""
        new_line = record.replace("\\ ", "\\")
        fields = new_line.split(" ")
        for i in fields:
            if (i == fields[2]):
                continue
            parts = i.split("=")
            dumb_array = (out_line, parts[1])
            out_line = "|".join(dumb_array)
        output = out_line.replace("\\"," ")
        return output
        
        
if __name__ == '__main__':
    reader = BroReader()
    for line in sys.stdin:
        result = reader.format(line)
        print result,
