from fping.backends import nmap
from fping.backends import fping
from fping.backends import ping

backends = {
    "nmap":   nmap.pinger_class,
    "fping": fping.pinger_class,
    "ping":   ping.pinger_class,
}

default_priority = ["fping", "nmap", "ping"]

def get_backend(priority=None, **kwargs):
    if not priority:
        priority = default_priority

    for name in priority:
        b = backends.get(name)
        if b:
            inst = b(**kwargs)
            if inst.is_available():
                return inst

    raise RuntimeError("No pinger backends Available")

backends = {
    "fping": fping.pinger_class,
}

def get_backend(priority=["fping"], **kwargs):
    for name in priority:
        b = backends.get(name)
        if b:
            inst = b(**kwargs)
            if inst.is_available():
                return inst

    raise RuntimeError("No pinger backends Available")

def ping_one(host):
    return get_backend().ping_one(host)

def ping_many_updown(hosts):
    return get_backend().ping_many_updown(hosts)

def ping_many_updown_iter(hosts):
    return get_backend().ping_many_updown_iter(hosts)

def ping_many(hosts):
    return get_backend().ping_many(hosts)

def ping_many_iter(hosts):
    return get_backend().ping_many_iter(hosts)