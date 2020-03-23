import json
from Jumpscale import j


class udp6proxy(j.baseclasses.threebot_actor):
    def _init(self, **kwargs):
        if j.sal.nettools.waitConnectionTest("127.0.0.1", port=6379, timeout=1):
            self.redisclient = j.clients.redis.get("127.0.0.1", port=6379)
        else:
            self._log_error(f"CONNECTION ERROR TO 127.0.0.1:6379")

    @j.baseclasses.actor_method
    def add_listener(
            self, name, local_port, remote_addr, remote_port, wg=False, prefix="", schema_out=None, user_session=None
    ):
        listener_dict = {
            "Name": name,
            "WireGuard": wg,
            "RemoteAddress": remote_addr,
            "RemotePort": remote_port,
            "LocalPort": local_port
        }
        self.redisclient.set(prefix+name, json.dumps(listener_dict))

    @j.baseclasses.actor_method
    def delete_listener(self, name, prefix="", schema_out=None, user_session=None):
        self.redisclient.delete(prefix+name)
