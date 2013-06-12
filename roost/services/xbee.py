from twisted.application import service
from twisted.python import log, usage
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys, os
import roost
from roost import events

from txXBee.protocol import txXBee

def _to_hex(source_addr):
  return ":".join("{0:x}".format(ord(c)) for c in source_addr)

class XBeeReader(txXBee):
  def __init__(self, *args, **kwds):
    super(XBeeReader, self).__init__(*args, **kwds)
    self.sources = set()

  def handle_packet(self, packet):
    source = _to_hex(packet['source_addr_long'])
    if not source in self.sources:
      events.fire('xbee.source.new', {"source": source, "samples": packet['samples']})
      self.sources.add(source)
    return events.fire('xbee.data', {"source": source, "samples": packet['samples']})

class XBeeService(service.Service):
  def __init__(self, opts={}):
    self.setName('xbee')
    self.device = opts.get('device', '/dev/ttyUSB0')
    self.reader = XBeeReader(escaped=True)

  def startService(self):
    if os.path.exists(self.device):
      service.Service.startService(self)
      self.port = SerialPort(self.reader, self.device, reactor, baudrate=9600)
    else:
      log.msg("Could not find device " + self.device)

  def properties(self):
    return {'sources': list(self.get_sources())}

  def get_sources(self):
    return [_to_hex(addr) for addr in self.reader.sources]

roost.add_service(XBeeService)
