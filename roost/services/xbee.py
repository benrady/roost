from twisted.application import service
from twisted.python import log
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys, os, pickle
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
    self.device = opts.get('xbee_device')
    self.reader = XBeeReader(escaped=True)
    self.opts = opts
    self.test_devices = None

  def _publish_test_data(self, data_dir):
    if not self.test_devices:
      self.test_devices = [open(data_dir + "/" + f) for f in os.listdir(data_dir)]
    for device in self.test_devices:
      try:
        self.reader.handle_packet(pickle.load(device))
      except EOFError:
        device.seek(0)
        self.reader.handle_packet(pickle.load(device))

  def _schedule_test_data(self, data_dir):
    l = task.LoopingCall(self._publish_test_data, data_dir)
    l.start(1.0)

  def startService(self):
    service.Service.startService(self)
    if os.path.exists(self.device):
      if os.path.isdir(self.device):
        self._schedule_test_data(self.device)
      else:
        self.port = SerialPort(self.reader, self.device, reactor, baudrate=9600)
    else:
      log.msg("Could not find device or directory" + self.device)

  def properties(self):
    return {'sources': list(self.get_sources())}

  def get_sources(self):
    return list(self.reader.sources)

roost.add_service(XBeeService)
