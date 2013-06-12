from twisted.application import service, internet
from twisted.internet import reactor
from twisted.web import server, resource, static

import roost

class ServiceResource(resource.Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
      return roost.services.find(request.postpath[0]).name

class Web(service.Service):
  def __init__(self, opts):
    self.setName('web')
    self.web_dir = opts.get('--web-dir', '/var/roost/www')

  def startService(self):
    service.Service.startService(self)
    root = static.File(self.web_dir) 
    root.putChild('services', ServiceResource())
    self.server = internet.TCPServer(8080, server.Site(root)).setServiceParent(self.parent)

roost.add_service(Web)
