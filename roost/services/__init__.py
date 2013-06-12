
import sys

_services = []
_started = []

def add(service):
  _services.append(service)

def find(service_name):
  return next(service for service in _started if service.name == service_name)

def start(app, opts):
  for s in [service_class(opts) for service_class in _services]:
    _started.append(s)
    s.setServiceParent(app)
