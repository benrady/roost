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

class XBeeReader(txXBee):
  def __init__(self, *args, **kwds):
    super(XBeeReader, self).__init__(*args, **kwds)
    self.sources = set()

  def handle_packet(self, packet):
    source = packet['source_addr_long']
    if not source in self.sources:
      events.fire('xbee.source.new', {"source": source, "packet": packet})
      self.sources.add(source)
    return events.fire('xbee.data', {"packet": packet})

class XBeeService(service.Service):
  def __init__(self, opts={}):
    self.setName('xbee')
    self.device = opts.get('--device', '/dev/ttyUSB0')
    self.reader = XBeeReader(escaped=True)

  def startService(self):
    if os.path.exists(self.device):
      service.Serice.startService(self)
      self.port = SerialPort(self.reader, ser_port_name, reactor, baudrate=9600)
    else:
      log.msg("Could not find device " + self.device)

  def get_sources(self):
    return self.reader.sources

roost.add_service(XBeeService)
