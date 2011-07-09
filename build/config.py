import ConfigParser

class ConfigFile():
    def __init__(self, file):
        
        self.config = ConfigParser.RawConfigParser()
        if file != 'None':
            self.config.read(file)
        else:
            self.config.read('gibson.conf')
        
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
    
    
