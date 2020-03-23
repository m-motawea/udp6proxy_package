from Jumpscale import j
import os

class Package(j.baseclasses.threebot_package):
    def prepare(self):
        server = self.openresty
        server.configure()

        website = server.get_from_port(port=80)
        locations = website.locations.get("udp6proxy")

        proxy_location = locations.get_location_proxy("udp6proxy")
        proxy_location.path_url = "/udp6proxy"
        proxy_location.ipaddr_dest = "127.0.0.1"
        proxy_location.port_dest = 12345
        proxy_location.type = "http"
        proxy_location.scheme = "http"
        proxy_location.is_auth = False

        locations.configure()
        website.configure()

        cmd_start = "python3 app.py"
        self.startupcmd = j.servers.startupcmd.get("udp6proxy", cmd_start=cmd_start,
                                                   path=os.path.abspath(os.path.join(__file__, os.pardir)))
        if not j.sal.fs.exists("/sandbox/bin/udp6proxy"):
            j.builders.network.udp6proxy.install()

    def start(self):
        return self.startupcmd.start()

    def stop(self):
        return self.startupcmd.stop()

