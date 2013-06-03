#!/usr/bin/env python

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

import os, sys, getopt
from roost import events, services

def parse_opts(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    opts, args = getopt.getopt(argv[1:], "d:w:", ["device=", "web-dir="])
    return dict(opts)
  except getopt.error, msg:
    raise Exception(msg)
    print >>sys.stderr, err.msg
    print >>sys.stderr, "for help use --help"

log.msg("Starting Roost")
if __name__ == "__main__":
  services.start(parse_opts());
  reactor.run()
else:
  from roost.services import xbee, env_sensors, web
  opts = { "--web-dir": 'web/public' }
  application = service.Application('roost')
  for service in services._services:
    service(opts).setServiceParent(application)

