from collections import OrderedDict

from pkg_resources import iter_entry_points

plugins = OrderedDict()
blocked_plugins = set([])


def load():
    for ep in iter_entry_points(".ext"):
        register(ep.load(), ep.name)


def register(module, name=None):
    if name is None:
        name = module.__name__
    if name in blocked_plugins:
        print("Requested registration of plugin {name} but this plugin is blocked")
        return
    plugins[name] = module


def spec(func):
    def caller(*args, **kwargs):
        for plugin in plugins.copy().values():
            try:
                getattr(plugin, func.__name__)(*args, **kwargs)
            except AttributeError:
                pass

    return caller


def block(name_or_module, reason=""):
    if not isinstance(name_or_module, str):
        name_or_module = name_or_module.__name__
    print(f"Blocking plugin {name_or_module}: {reason}")
    if name_or_module in plugins:
        del plugins[name_or_module]
    blocked_plugins.add(name_or_module)


@spec
def register_http_endpoint(api):
    """Add new endpoints to Geocode API."""


@spec
def register_http_middleware(middlewares):
    """Add new middlewares to Geocode API."""


@spec
def preconfigure(config):
    """Configure addok by patching config object before user local config."""


@spec
def configure(config):
    """Configure addok by patching config object after user local config."""


@spec
def register_command(subparsers):
    """Register command for Geocode CLI."""


@spec
def register_shell_command(cmd):
    """Register command for Geocode shell."""
