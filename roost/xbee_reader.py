from twisted.python import log, usage
from twisted.internet import reactor, task
from twisted.internet.serialport import SerialPort
from twisted.web.http_headers import Headers

from struct import unpack

import sys

from txXBee.protocol import txXBee

class MyOptions(usage.Options):
	optParameters = [
		['outfile', 'o', None, 'Logfile [default: sys.stdout]'],
		['baudrate', 'b', 38400, 'Serial baudrate [default: 38400'],
		['port', 'p', '/dev/tty.usbserial-A600ezgH', 'Serial Port device'],
	]

devices = {
	"template": "\x00\x13\xA2\x00\x00\x00\x00\x00",
	"template1": "\x00\x13\xA2\x00\x00\x00\x00\x00",
	"template2": "\x00\x13\xA2\x00\x00\x00\x00\x00",
}

class YourWrapperName(txXBee):
  def __init__(self, *args, **kwds):
    super(YourWrapperName, self).__init__(*args, **kwds)

  def handle_packet(self, xbeePacketDictionary):
    response = xbeePacketDictionary # FIXME This is all we need?
    print response

  def getSomeData(self):
    reactor.callFromThread(self.send,
      "tx",
      frame_id="\x01",
      dest_addr_long=devices["template1"],
      dest_addr="\xff\xfe",
      data="SEND_ME_SOME_DATA")

def open_port(ser_port_name):
  return SerialPort(YourWrapperName(escaped=True), ser_port_name, reactor, baudrate=9600)
