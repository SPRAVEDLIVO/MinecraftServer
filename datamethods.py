class Position(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_pos(self):
        return ((self.x & 0x3FFFFFF) << 38) | ((self.y & 0xFFF) << 26) | (self.z & 0x3FFFFFF)
    @property
    def dump(self):
        return "{0}(x={1} y={2} z={3})".format("Position", self.x, self.y, self.z)

    def get_xyz(self):
        return {'x':self.x, 'y':self.y, 'z':self.z}