import plugin
event = plugin.Event()
command = plugin.Command()
@event.event("on_join")
def on_join(player, addr):
    print(player, addr)
@command.event("login")
def cmd(nargs):
    print(nargs)