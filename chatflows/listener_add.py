from Jumpscale import j
import gevent
import redis
import json


def chat(bot):
    name = bot.string_ask("What is the listener Name?")
    remote_addr = bot.string_ask("What is the remote IPv6 address?")
    remote_port = bot.int_ask("What is the remote port?")
    local_port = bot.int_ask("What is the local port to bind to?")
    wg = bot.single_choice("Is this a WireGuard endpoint?", ["yes", "no"])
    if wg == "yes":
        wg = True
    else:
        wg = False
    prefix = bot.string_ask("What is redis prefix?")
    listener_dict = {
        "Name": name,
        "RemoteAddress": remote_addr,
        "RemotePort": remote_port,
        "LocalPort": local_port,
        "WireGuard": wg
    }
    cl = redis.Redis()
    cl.set(prefix+name, json.dumps(listener_dict))
    res = """
    Name: {{Name}}
    RemoteAddress: {{RemoteAddress}}
    RemotePort: {{RemotePort}}
    LocalPort: {{LocalPort}}
    WireGuard: {{WireGuard}}
    Prefix: {{Prefix}}
    """
    bot.template_render(res, **listener_dict, Prefix=prefix)