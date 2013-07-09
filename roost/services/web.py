from twisted.application import service, internet
from twisted.internet import reactor
from twisted.web import server, resource, static
from twisted.python import log
from autobahn import websocket

import json
import roost

class ServiceResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
      service = roost.services.find(request.postpath[0])
      if request.postpath[1] == 'properties':
        return json.dumps(service.properties.export())

class EventsWebsocket(websocket.WebSocketServerProtocol):
  def onMessage(self, msg, binary):
    roost.listen_to(msg, self.on_event)

  def on_event(self, event, data):
    self.sendMessage(json.dumps({'event': event, 'eventData': data}), False)

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
    factory = websocket.WebSocketServerFactory("ws://localhost:9090")
    factory.protocol = EventsWebsocket
    websocket.listenWS(factory)

roost.add_service(Web)
