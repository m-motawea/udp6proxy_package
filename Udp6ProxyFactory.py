from Jumpscale import j


class Udp6ProxyFactory(j.baseclasses.object, j.baseclasses.testtools):

    __jslocation__ = "j.threebot_factories.package.udp6proxy"

    def start(self):
        """
        kosmos 'j.threebot.package.udp6proxy.start()'
        :return:
        """
        gedis_client = j.servers.threebot.start()
        gedis_client.actors.package_manager.package_add(path=self._dirpath)