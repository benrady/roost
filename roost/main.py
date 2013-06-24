#!/usr/bin/env python

from twisted.internet import reactor
from twisted.python import log
from twisted.application import service
from twisted.conch import manhole_tap

from roost import events, services
from roost.services import xbee, env_sensors, web


def telnet_service(user_file):
  import roost
  namespace = {'roost': roost, 'xbee': roost.find_service('xbee')}
  shell_options = {
    'namespace'  : namespace,
    'passwd'     : user_file,
    'sshPort'    : None,
    'telnetPort' : '4040',
  }
  return manhole_tap.makeService(shell_options)

def makeService(config):
  log.msg("Starting Roost")
  top_service = service.MultiService()
  services.start(top_service, config)
  if config.has_key('telnet-users'):
    telnet_service(config['telnet-users']).setServiceParent(top_service)
  return top_service
