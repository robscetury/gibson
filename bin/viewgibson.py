#!env ppython
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:40:21 2010

@author: -
"""
from optparse import OptionParser
import sys
import xml.sax
from xml.sax.handler import feature_namespaces, ContentHandler
import gibson
import traceback
# Main
if __name__ == '__main__':
    from gibson.programs import network
    from gibson import parse_nmap

    option_parser = OptionParser()
    option_parser.add_option("-x", "--xml", dest="xmlfile", help="XMLFILE to use as input", metavar="XMLFILE")
    option_parser.add_option("-c", "--config", dest="configfile", help="read configuration from FILE", metavar="FILE")
    (options, args) = option_parser.parse_args()

    #threedee_math = threedee_math.threedee_math()
    parser = xml.sax.make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = parse_nmap.ImportServer()
    parser.setContentHandler(dh)
    try:
        print gibson.getPath("xml", options.xmlfile)
        parser.parse(gibson.getPath("xml", options.xmlfile))
    except:
        traceback.print_exc()
        print "You have not specified an xml model. I'll assume you know what you're doing...."

    scene = network.Panda(options)
    scene.run()
