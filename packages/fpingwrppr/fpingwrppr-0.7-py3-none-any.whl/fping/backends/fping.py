import subprocess, os, tempfile
from fping.backends.base import BasePinger

def os_wait():
    try:
        os.wait()
    except OSError:
        pass

class FpingPinger(BasePinger):
    program = "fping"
    help_return_code = 3

    def ping_many_updown_iter(self, hosts, fast=False):
        """Ping a list of IPs, return an iterator of state, node"""
        cmd = [self.program_path]
        if fast:
            cmd.extend(["-r", "1", "-t", "100"])

        with subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, close_fds=True) as sub:
            for ip in hosts:
                sub.stdin.write(f"{ip}\n")
            sub.stdin.close()

            up = []
            down = []
            for line in sub.stdout:
                line = line.strip()
                ip, _, status = line.partition(" ")
                if status == "is alive":
                    yield 'up', ip
                elif status == "is unreachable":
                    yield 'down', ip

        os_wait()

    def ping_many_updown(self, hosts, fast=False):
        """Ping a list of IPs, return a tuple of (up nodes, down nodes)"""
        up = []
        down = []
        lists = dict(up=up, down=down)
        for state, ip in self.ping_many_updown_iter(hosts, fast):
            lists[state].append(ip)
        return up, down

pinger_class = FpingPinger