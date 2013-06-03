from twisted.application import service, internet
from twisted.internet import reactor
from twisted.web import server, resource, static

import roost

#class Simple(resource.Resource):
#    isLeaf = True
#    def render_GET(self, request):
#        return "<html>Hello, world!</html>"

class Web(service.Service):
  def __init__(self, opts):
    self.setName('Web')
    self.web_dir = opts.get('--web-dir', '/var/roost/www')

  def startService(self):
    service.Service.startService(self)
    root = static.File(self.web_dir) 
    #root.putChild('events', Simple())
    self.server = internet.TCPServer(8080, server.Site(root)).setServiceParent(self.parent)

roost.add_service(Web)
