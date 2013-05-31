#!/usr/bin/env python

from twisted.web import server, resource, static
from twisted.internet import reactor

import xbee_reader, events
import os, sys, getopt

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

def start_reactor(opts):
  web_dir = opts.get('--web-dir', '/var/roost/www')
  device = opts.get('--device', '/dev/ttyUSB0')
  root = static.File(web_dir) 
  root.putChild('events', Simple())
  reactor.listenTCP(8080, server.Site(root))
  if os.path.exists(device):
    xbee_reader.open_port(device)
  else:
    print >>sys.stderr, "Could not find device " + device
  print "Starting Roost"
  events.fire('roost.startup')
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
