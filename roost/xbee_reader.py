from twisted.python import log, usage
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys, roost

from txXBee.protocol import txXBee

class XBeeReader(txXBee):
  def __init__(self, *args, **kwds):
    super(XBeeReader, self).__init__(*args, **kwds)

  def handle_packet(self, packet):
    roost.fire_event('xbee.data', {"packet": packet})

  def getSomeData(self):
    reactor.callFromThread(self.send,
      "tx",
      frame_id="\x01",
      dest_addr_long=devices["template1"],
      dest_addr="\xff\xfe",
      data="SEND_ME_SOME_DATA")

def open_port(ser_port_name):
  return SerialPort(XBeeReader(escaped=True), ser_port_name, reactor, baudrate=9600)
