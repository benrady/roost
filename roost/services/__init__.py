
import sys

_services = []

def add(service):
  _services.append(service)

def start(options):
  import env_sensors, xbee, web
  # Should use the IMultiService interface for this
  for service in _services:
    service(options).startService()
