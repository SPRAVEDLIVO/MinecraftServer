from quarry.net.server import ServerFactory, ServerProtocol
import plugin
import datamethods

players = {}
iterable_id = 0

class MineServer(ServerProtocol):
    @property
    def id(self):
        global iterable_id
        iterable_id += 1
        return iterable_id
    def player_joined(self):
        ServerProtocol.player_joined(self)
