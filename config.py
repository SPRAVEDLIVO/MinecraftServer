import configparser
class Config(object):
    def __init__(self, path="server.properties", section="PROPERTIES"):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path)
        self.section = section
    def GetBoolean(self, option):
        return self.config.getboolean(option=option, section=self.section)
    def GetFloat(self, option):
        return self.config.getfloat(option=option, section=self.section)
    def GetInt(self, option):
        return self.config.getint(option=option, section=self.section)
    def Get(self, option):
        return self.config.get(option=option, section=self.section)