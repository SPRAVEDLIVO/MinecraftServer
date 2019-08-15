"""
Example "chat room" server

This server authenticates players, then spawns them in an empty world and does
the bare minimum to keep them in-game. Players can speak to eachother using
chat.

Supports Minecraft 1.14. Earlier versions will not work as the packet formats
differ.
"""

from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol


class ChatRoomProtocol(ServerProtocol):
    def player_joined(self):
        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)

        # Send "Join Game" packet
        self.send_packet("join_game",
            self.buff_type.pack("iBiB",
                0,                              # entity id
                1,                              # game mode
                0,                              # dimension
                0),                             # max players
            self.buff_type.pack_string("flat"), # level type
            self.buff_type.pack_varint(100),      # view distance
            self.buff_type.pack("?", False))    # reduced debug info

        # Send "Player Position and Look" packet
        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                0,                         # x
                25,                       # y
                0,                         # z
                0,                         # yaw
                0,                         # pitch
                0b00000),                  # flags
            self.buff_type.pack_varint(0)) # teleport id

        # Start sending "Keep Alive" packets
        self.ticker.add_loop(20, self.update_keep_alive)

        # Announce player joined
        self.factory.send_chat(u"\u00a7e%s has joined." % self.display_name)

    def player_left(self):
        ServerProtocol.player_left(self)

        # Announce player left
        self.factory.send_chat(u"\u00a7e%s has left." % self.display_name)

    def update_keep_alive(self):
        # Send a "Keep Alive" packet

        # 1.7.x
        if self.protocol_version <= 338:
            payload =  self.buff_type.pack_varint(0)

        # 1.12.2
        else:
            payload = self.buff_type.pack('Q', 0)

        self.send_packet("keep_alive", payload)

    def packet_chat_message(self, buff):
        # When we receive a chat message from the player, ask the factory
        # to relay it to all connected players
        p_text = buff.unpack_string()
        self.factory.send_chat("<%s> %s" % (self.display_name, p_text))


class ChatRoomFactory(ServerFactory):
    protocol = ChatRoomProtocol
    motd = "Chat Room Server"

    def send_chat(self, message):
        for player in self.players:
            player.send_packet("chat_message",player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0) )


def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default="", help="address to listen on")
    parser.add_argument("-p", "--port", default=25565, type=int, help="port to listen on")
    args = parser.parse_args(argv)

    # Create factory
    factory = ChatRoomFactory()
    factory.online_mode = False
    # Listen
    factory.listen(args.host, args.port)
    reactor.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])