from twisted.application import service
from twisted.python import log
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys, os, pickle
import roost
from roost import events, properties

from txXBee.protocol import txXBee

def _to_hex(source_addr):
  return ":".join("{0:x}".format(ord(c)) for c in source_addr)

def _from_hex(source):
  return "".join([chr(int(b, 16)) for b in source.split(":")])

class XBeeReader(txXBee):
  def __init__(self, *args, **kwds):
    super(XBeeReader, self).__init__(*args, **kwds)
    self.on_packet = None
    self.print_packets = False

  def handle_packet(self, packet):
    if self.print_packets:
      print packet
    if self.on_packet: self.on_packet(packet)

class XBeeService(service.Service):
  def __init__(self, opts={}):
    self.setName('xbee')
    self.device = opts.get('xbee_device')
    self.reader = XBeeReader(escaped=True)
    self.reader.on_packet = self._on_packet
    self.opts = opts
    self.sources = {}
    self.test_devices = None
    self.properties = properties.Properties(defaults={'sources':{}})

  def _new_source(self):
    return dict()

  def _on_packet(self, packet):
    source = _to_hex(packet['source_addr_long'])
    if not source in self.sources:
      self.sources[source] = {'source_addr_long': packet['source_addr_long'], 'source_addr': packet['source_addr']}
      events.fire('xbee.new', {'source': source, 'samples': packet.get('samples', [])})
    if packet.has_key('samples'):
      data = {"source": source, "samples": packet['samples'], 'source_addr': _to_hex(packet['source_addr'])}
      return events.fire('xbee.data', data)

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

  def get_sources(self):
    return self.sources

  # http://www.digi.com/support/kbase/kbaseresultdetl?id=3221
  # https://code.google.com/p/python-xbee/source/browse/xbee/zigbee.py#35
  def send_at_command(self, device_addr, command):
    source = self.sources[device_addr]
    return reactor.callFromThread(self.reader.send,
      'remote_at', 
      dest_addr_long=source['source_addr_long'], 
      dest_addr=source['source_addr'], 
      command=command)

roost.add_service(XBeeService)
