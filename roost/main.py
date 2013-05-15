#!/usr/bin/env python

from twisted.web import server, resource, static
from twisted.internet import reactor

#from xbee_reader import open_port

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

def main(device='/dev/ttyUSB0', data_dir='/var/roost/data'):
  root = static.File('public') # FIXME This should be a parameter
  root.putChild('hello', Simple())
  reactor.listenTCP(8080, server.Site(root))
  #xbee_reader.open_port(device)
  reactor.run()

if __name__ == "__main__":
  main()
