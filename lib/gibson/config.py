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
import ConfigParser
from gibson import *
class ConfigFile():
    def __init__(self, file):
        
        self.config = ConfigParser.RawConfigParser()
        if file != 'None':
            file = getPath("conf", file)


        else:
            file = getPath("conf", "gibson.conf")

        self.config.read(file)
        
    def skybox_texture(self):        
        try:
            return self.config.get('Display', 'background')
        except ConfigParser.NoOptionError:
            return 0
    
    def bg_color(self):
        try:
            return self.config.get('Display', 'background_color')
        except ConfigParser.NoOptionError:
            return 0
            
    def skyshape(self):
        try:
            return self.config.get('Display', 'skyshape')
        except ConfigParser.NoOptionError:
            return 0
    def slug_speed(self):
        try:
            return self.config.get('Display', 'slug_speed')
        except ConfigParser.NoOptionError:
            return 60

    def slug_timeout(self):
        try:
            return self.config.get('Display', 'slug_timeout')
        except ConfigParser.NoOptionError:
            return 300


    def autobuild(self):
        try:
            return self.config.get('Display', 'autobuild_model')
        except ConfigParser.NoOptionError:
            return 0
        
    def zone_list(self):
        try:
            return self.config.get('Network', 'security_zones')
        except ConfigParser.NoOptionError:
            print "You must define at least one security zone in the \n security_zones variable in your config file."
            raise
        
    def subnet(self, name):
        try:
            return self.config.get('Network', name)
        except ConfigParser.NoOptionError:
            print "You must define at least one security zone in the \n security_zones variable in your config file."
            raise
        
        
    def xml_file(self):
        try:
            return self.config.get('Network', 'XML_file')
        except ConfigParser.NoOptionError:
            return 0
    


    def routers(self):
        try:
            items = self.config.items('Network')
            routers = []
            for i in items:
                if 'router' in i[0]:
                    routers.append(i[1])
            return routers
        except ConfigParser.NoOptionError:
            return 0
