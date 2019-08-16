import plugin, server
event = plugin.Event()
command = plugin.Command()
@event.event("on_join")
def on_join(player, addr):
    print(player, addr)
@command.event("login")
def cmd(nargs):
    print(nargs)
@event.event("selfevent")
def tp(s, cmd, nargs):
    if cmd == "tp":
        try:
            x = float(nargs[0])
            y = float(nargs[1])
            z = float(nargs[2])
            s.send_position_and_look(x, y, z, 0, 0)
        except:
            s.send_chat('Incorrect coords')
            s.send_error = False