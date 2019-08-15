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
level_type = str(props.Get("level-type")).lower()

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
    def send_game(self, entity_id, gamemode, dimension, max_players, level_type, view_distance, debug_info=False):
        self.send_packet("join_game",
            self.buff_type.pack("iBiB",
                entity_id,                              # entity id
                gamemode,                              # game mode
                dimension,                              # dimension
                max_players),                             # max players
            self.buff_type.pack_string(level_type), # level type
            self.buff_type.pack_varint(view_distance),      # view distance
            self.buff_type.pack("?", debug_info))    # reduced debug info
    def packet_chat_message(self, buff):
        p_text = buff.unpack_string()
        if not "/" in p_text:
            self.logger.info("<%s> %s" % (self.display_name, p_text))
            self.factory.send_chat("<%s> %s" % (self.display_name, p_text))
        else:
            self.factory.send_chat("command executed!")
    def send_spawn_pos(self, position):  # args: (x, y, z) int
        self.send_packet("spawn_position",
                         self.buff_type.pack('q', position.get_pos())  # get_pos() is long long type
                         )
    def send_position_and_look(self, x, y, z, yaw, pitch, flags=0b00000, tp_id=0):
        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                x,                         # x
                y,                       # y
                z,                         # z
                yaw,                         # yaw
                pitch,                         # pitch
                flags),                  # flags
            self.buff_type.pack_varint(tp_id)) # teleport id
    def update_keep_alive(self):
        if self.protocol_version <= 338:
            payload =  self.buff_type.pack_varint(0)
        else:
            payload = self.buff_type.pack('Q', 0)
        self.send_packet("keep_alive", payload)
    def send_empty_chunk(self, x, z):  # args: chunk position ints (x, z)
        self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))
    def send_abilities(self, flying, fly, god, creative, fly_speed,
                       walk_speed):  # args: bool (if flying, if can fly, if no damage, if creative, (num) fly speed, walk speed)
        bitmask = 0
        if flying: bitmask = bitmask | 0x02
        if fly: bitmask = bitmask | 0x04
        if god: bitmask = bitmask | 0x08
        if creative: bitmask = bitmask | 0x01
        self.send_packet("player_abilities", self.buff_type.pack('bff', bitmask, float(fly_speed), float(walk_speed)))
    def player_joined(self):
        ServerProtocol.player_joined(self)
        self.ip = self.remote_addr.host
        self.position = Position(0, 66, 0)
        self.entity_id = self.id
        display_name = self.display_name
        addr = self.remote_addr.host
        print("[*] Player {} loggined in with IP {}".format(display_name, addr))
        self.send_game(0, default_gamemode, default_dimension, max_players, level_type, 10)
        self.send_spawn_pos(self.position)
        self.send_abilities(True, True, True, True, 0.2, 0.2)
        self.send_position_and_look(0, 25, 25, 0, 0)
        #self.send_empty_chunk(0, 0)
        self.factory.send_chat("Welcome to a MinecraftServer")
        self.ticker.add_loop(20, self.update_keep_alive)
    #def player_left(self):
    #    del players[self.entity_id]
    #    ServerProtocol.player_left(self)
class MineFactory(ServerFactory):
    protocol = MineServer
    def send_chat(self, message):
        for player in self.players:
            player.send_packet("chat_message",player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0) )
#portotype of server start
def main():
    factory = MineFactory()
    factory.motd = motd
    factory.listen(host, port)
    factory.max_players = max_players
    factory.online_mode = online_mode
    reactor.run()
main()