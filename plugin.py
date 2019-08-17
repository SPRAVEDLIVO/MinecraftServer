import importlib, os
events = {}
commands = {}
plugins = {}
banned = ['__pycache__']
def main():
    for pl in os.listdir("plugins/"):
        if pl not in banned:
            path = pl.replace(".py", "")
            spec = importlib.util.spec_from_file_location(path, "plugins/{}".format(pl))
            foo = importlib.util.module_from_spec(spec)
            plugins.update({path:foo})
            spec.loader.exec_module(foo)
def dynamic_reload(module):
    for k, v in plugins.items():
        if k == module:
            plugins.update({k:importlib.reload(v)})
def reload_all():
    for k, v in plugins.items():
        plugins.update({k:importlib.reload(v)})
def dynamic_import(module):
    spec = importlib.util.spec_from_file_location(module, "plugins/{}.py".format(module))
    foo = importlib.util.module_from_spec(spec)
    plugins.update({module:foo})
    spec.loader.exec_module(foo)
class Event(object):
    def SetEvent(self, event, s, *args):
        for d in events.get(event):
            for func, req in d.items():
                if req == "default":
                    func(*args)
                elif req == "self":
                    func(s, *args)
    def event(self, event, require="default"):
        def func_wrap(func):
            if event not in events.keys():
                events.update({event:[{func:require}]})
            else:
                events.get(event).append({func:require})
        return func_wrap
class Command(object):
    def event(self, command, require="default"):
        def func_wrap(func):
            if command not in commands.keys():
                commands.update({command:[{func:require}]})
            else:
                commands.get(command).append({func:require})
        return func_wrap
def SetCommand(command, args, s):
    assert type(args) == list
    if command in commands.keys():
        for d in commands.get(command):
            for func, req in d.items():
                if req == "default":
                    func(args)
                elif req == "self":
                    func(s, args)
    else:
        return False