#!/usr/bin/env python

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service

from roost import events, services
from roost.services import xbee, env_sensors, web

def makeService(config):
  log.msg("Starting Roost")
  top_service = service.MultiService()
  services.start(top_service, config)
  return top_service
