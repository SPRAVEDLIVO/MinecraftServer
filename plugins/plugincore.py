import plugin, server, os
from twisted.internet import reactor
event = plugin.Event()
command = plugin.Command()
@event.event("on_join", require="self")
def on_join(s, player, addr):
    print(player, addr)
    s.send_chat("Player %s has joined the server." % player)
@command.event("login")
def cmd(nargs):
    print(nargs)
@command.event("tp", require="self")
def plugincore(s, nargs):
    try:
        x = float(nargs[0])
        y = float(nargs[1])
        z = float(nargs[2])
        s.send_position_and_look(x, y, z, 0, 0)
    except:
        s.send_chat('Incorrect coords')
        s.send_error = False
@command.event("stop", require="self")
def stop(s, nargs):
    s.logger.info("[*] Player %s stopped the server." % s.display_name)
    s.factory.send_chat("Stopping..")
    s.close("Server have been stopped.")
    reactor.removeAll()
    reactor.iterate()
    reactor.stop()
    os._exit(0)