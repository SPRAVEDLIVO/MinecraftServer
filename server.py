from quarry.net.server import ServerFactory, ServerProtocol
import datamethods
import config
from twisted.internet import reactor
from datamethods import Position
import plugin
plugin.main()
event = plugin.Event()
command = plugin.Command()

props = config.Config()
host = props.Get("server-ip")
port = props.GetInt("server-port")
default_gamemode = props.GetInt("gamemode")
default_difficulty = props.GetInt("difficulty")
motd = props.Get("motd")
max_players = props.GetInt("max-players")
default_dimension = 0
online_mode = props.GetBoolean("online-mode")
level_type = props.Get("level-type").lower()

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
    def send_chat(self, message_bytes, position=0):  # args: (message[str], position[int])
        self.send_packet('chat_message',
                         self.buff_type.pack_chat(message_bytes) +
                         self.buff_type.pack('b', position)
                         )
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
    def send_change_game_state(self, reason, state):
        self.send_packet("change_game_state", self.buff_type.pack('Bf', reason, state))
    def packet_chat_message(self, buff):
        p_text = buff.unpack_string()
        if p_text[0] != '/':
            self.factory.send_chat("<%s> %s" % (self.display_name, p_text))
        else:
            txt = p_text[1:].split(" ")
            command = txt[0]
            nargs = p_text.split(' ')[1:]
            if plugin.SetCommand(command, nargs, self) == False and self.send_error:
                self.send_chat("Unknown command!")
            self.send_error = True
        self.logger.info("<%s> %s" % (self.display_name, p_text))
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
        self.send_packet("chunk_data", 0x1001880C0060020)
        #self.send_packet("chunk_data", self.buff_type.pack('ii?H', x, z, True, 0) + self.buff_type.pack_varint(0))
    def set_slot(self):
        self.send_packet("set_slot", self.buff_type.pack('BH?', 0, 3, True) + self.buff_type.pack_varint(5))
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
        self.send_game(0, default_gamemode, default_dimension, max_players, level_type, 10)
        self.send_spawn_pos(self.position)
        self.send_abilities(True, True, True, True, 0.2, 0.2)
        self.send_position_and_look(0, 25, 25, 0, 0)
        self.send_error = True
        #self.send_empty_chunk(0, 0)
        self.ticker.add_loop(20, self.update_keep_alive)
        event.SetEvent("on_join", display_name, addr)
    def player_left(self):
        ServerProtocol.player_left(self)
        event.SetEvent("on_leave", self.display_name, self.remote_addr.host)
    def set_position(self, x, y, z, xr=0, yr=0, on_ground=False):
        self.position.set(x, y, z)
        self.send_position_and_look(self.position, xr, yr, 0, on_ground)
class MineFactory(ServerFactory):
    protocol = MineServer
    def send_chat(self, message):
        for player in self.players:
            player.send_packet("chat_message",player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0) )
#portotype of server start
def main():
    factory = MineFactory()
    factory.motd = motd
    factory.max_players = max_players
    factory.online_mode = online_mode
    factory.listen(host, port)
    reactor.run()
main()