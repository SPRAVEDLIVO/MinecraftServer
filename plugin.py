# Please implement this later...
import importlib.util, os
events = {}
commands = {}
def main():
    for pl in os.listdir("plugins/"):
        if pl not in ['__pycache__']:
            path = pl.replace(".py", "")
            spec = importlib.util.spec_from_file_location(path, "plugins/{}".format(pl))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
class Event(object):
    def SetEvent(self, event, *args):
        if event not in events.keys():
            events.update({event:[]})
        for func in events.get(event):
            func(*args)
    def event(self, event):
        def func_wrap(func):
            if event not in events.keys():
                events.update({event:[func]})
            else:
                events.get(event).append(func)
        return func_wrap
class Command(object):
    def event(self, command):
        def func_wrap(func):
            if command not in commands.keys():
                commands.update({command:[func]})
            else:
                commands.get(command).append(func)
        return func_wrap
def SetCommand(command, args):
    assert type(args) == list
    if command in commands.keys():
        for func in commands.get(command):
            func(args)
    else:
        return False