#!/usr/bin/env python

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

from roost import events, services
from roost.services import xbee, env_sensors, web

log.msg("Starting Roost")
opts = { 
  "web-dir": 'web/public',
  'device': '/dev/tty.usbserial-A901JXEE'
}
application = service.Application('roost')
services.start(application, opts)
