#!/usr/bin/env python

from twisted.web import server, resource, static
from twisted.internet import reactor

import xbee_reader
import sys, getopt

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

def start_reactor(opts):
  web_dir = opts.get('--web-dir', '/var/roost/www')
  device = opts.get('--device', '/dev/ttyUSB0')
  print "Starting Roost"
  root = static.File(web_dir) 
  root.putChild('events', Simple())
  reactor.listenTCP(8080, server.Site(root))
  #xbee_reader.open_port(device)
  reactor.run()

def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    opts, args = getopt.getopt(argv[1:], "d:w:", ["device=", "web-dir="])
    return start_reactor(dict(opts));
  except getopt.error, msg:
    raise Exception(msg)
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main());
