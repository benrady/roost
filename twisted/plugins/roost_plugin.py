# ==== twisted/plugins/twist_plugin.py ====
# - Zope modules -
from zope.interface import implements

# - Twisted modules -
from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin

# - twist modules -
from roost import main

class Options(usage.Options):
    synopsis = "[options]"
    longdesc = "Start the roost service"
    optParameters = [
        ['xbee_device', 'x', 'testdata/devices', 'Path to the XBee controller radio or pickled packet files'],
        ['port', 'p', '8080', 'Web application port'],
        ['telnet-users', 't', 'deb/users.txt'],
        ['web-dir', 'w', 'web/public', 'Web application files'],
    ]

class MyServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    
    tapname = "roost"
    description = "roost server."
    options = Options
    
    def makeService(self, config):
        return main.makeService(config)

serviceMaker = MyServiceMaker()
