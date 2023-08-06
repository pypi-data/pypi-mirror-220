from fping.backends import fping

back = {"fping": fping.pinger_class}

def get_backend(priority=None, **kwargs):
    if not priority:
        priority = ["fping"]

    for name in priority:
        b = back.get(name)
        if b:
            inst = b(**kwargs)
            if inst.is_available():
                return inst

    raise RuntimeError("No pinger backends Available")

def ping(host):
    return get_backend().ping(host)

def ping_many_updown(hosts):
    return get_backend().ping_many_updown(hosts)

def ping_many_updown_iter(hosts):
    return get_backend().ping_many_updown_iter(hosts)

def ping_many(hosts):
    return get_backend().ping_many(hosts)

def ping_many_iter(hosts):
    return get_backend().ping_many_iter(hosts)