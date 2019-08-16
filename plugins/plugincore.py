import plugin, server, os
from twisted.internet import reactor
event = plugin.Event()
command = plugin.Command()
@event.event("on_join")
def on_join(player, addr):
    print(player, addr)
@command.event("login")
def cmd(nargs):
    print(nargs)
@event.event("selfevent")
def plugincore(s, cmd, nargs):
    if cmd == "tp":
        try:
            x = float(nargs[0])
            y = float(nargs[1])
            z = float(nargs[2])
            s.send_position_and_look(x, y, z, 0, 0)
        except:
            s.send_chat('Incorrect coords')
            s.send_error = False
    elif cmd == "stop":
        s.logger.info("[*] Player %s stopped the server." % s.display_name)
        s.factory.send_chat("Stopping..")
        s.close("Server have been stopped.")
        reactor.removeAll()
        reactor.iterate()
        reactor.stop()
        os._exit(0)