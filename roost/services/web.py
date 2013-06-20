from twisted.application import service, internet
from twisted.internet import reactor
from twisted.web import server, resource, static
from twisted.python import log

import json
import roost

class ServiceResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
      service = roost.services.find(request.postpath[0])
      if request.postpath[1] == 'properties':
        return json.dumps(service.properties())

class Web(service.Service):
  def __init__(self, opts):
    self.setName('web')
    self.web_dir = opts.get('web-dir')
    self.port = int(opts.get('port'))

  def properties(self):
    return {}

  def startService(self):
    service.Service.startService(self)
    root = static.File(self.web_dir) 
    root.putChild('services', ServiceResource())
    self.server = internet.TCPServer(self.port, server.Site(root)).setServiceParent(self.parent)

roost.add_service(Web)
