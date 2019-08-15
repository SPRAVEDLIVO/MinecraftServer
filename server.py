from quarry.net.server import ServerFactory, ServerProtocol
import datamethods
import config
from twisted.internet import reactor
from datamethods import Position

props = config.Config()
host = props.Get("server-ip")
port = props.GetInt("server-port")
default_gamemode = props.GetInt("gamemode")
default_difficulty = props.GetInt("difficulty")
motd = props.Get("motd")
max_players = props.GetInt("max-players")
default_dimension = 0
online_mode = props.GetBoolean("online-mode")

players = {}
iterable_id = 0

class MineServer(ServerProtocol):
    def packet_login_start(self, buff):
        ServerProtocol.packet_login_start(self, buff)
    @property
    def id(self):
        global iterable_id
        iterable_id += 1
        return iterable_id
    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.ip = self.remote_addr.host
        self.position = Position(0, 66, 0)
        self.entity_id = self.id
        display_name = self.display_name
        addr = self.remote_addr.host
        print("[*] Player {} loggined in with IP {}".format(display_name, addr))
        self.close("Passed")
    #def player_left(self):
    #    del players[self.entity_id]
    #    ServerProtocol.player_left(self)
class MineFactory(ServerFactory):
    protocol = MineServer
#portotype of server start
def main():
    factory = MineFactory()
    factory.motd = motd
    factory.listen(host, port)
    factory.max_players = max_players
    factory.online_mode = online_mode
    reactor.run()
main()