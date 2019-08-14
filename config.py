import configparser
class Config(object):
    def __init__(self, path="server.properties", section="PROPERTIES"):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path)
        self.section = section
    def GetBoolean(self, option, section=self.section):
        return self.config.getboolean(section, option)
    def GetFloat(self, option, section=self.section):
        return self.config.getfloat(section, option)
    def GetInt(self, option, section=self.section):
        return self.config.getint(section, option)
    def Get(self, option, section=self.section):
        return self.config.get(section, option)