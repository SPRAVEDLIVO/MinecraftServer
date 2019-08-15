# Please implement this later...
class Plugin(object):
    def __init__(self, path='./plugins'):
        self.path = path
    class Event(Plugin):
        def create(self, func, bool, funcafter):
            pass
pl = Plugin()
def mp():
    print("de")