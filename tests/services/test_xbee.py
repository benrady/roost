from roost.services import xbee
from roost import events
from nose.tools import * 
from mock import Mock

import types, unittest, shutil, os

class TestXBeeReader(unittest.TestCase):

  def setUp(self):
    self.reader = xbee.XBeeReader()
    self.packet_samples = [{'adc-0': 605, 'adc-1': 570}]
    self.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': self.packet_samples, 'options': '\x01'} 
    events.fire = Mock()

  def test_handle_packet(self):
    self.reader.handle_packet(self.packet)
    events.fire.assert_called_with('xbee.data', {
      "source": '0:13:a2:0:40:89:e5:43',
      "samples": self.packet_samples})

  def test_new_source(self):
    self.reader.handle_packet(self.packet)
    events.fire.assert_any_call('xbee.source.new', {
      "source": '0:13:a2:0:40:89:e5:43',
      "samples": self.packet_samples
    })
    eq_(self.reader.sources, set([xbee._to_hex(self.packet['source_addr_long'])]))

  def test_existing_source(self):
    self.reader.handle_packet(self.packet)
    self.reader.handle_packet(self.packet)
    eq_(events.fire.call_count, 3) # Would be four times if the source weren't new

  def test_to_hex(self):
    eq_("0:13:a2:0:40:89:e5:43", xbee._to_hex(self.packet['source_addr_long']))

class TestXBeeService(unittest.TestCase):
  def setUp(self):
    self.service = xbee.XBeeService()

  def test_no_sources_by_default(self):
    eq_(self.service.get_sources(), [])

  def test_properties(self):
    eq_(self.service.properties(), {'sources': []})

  def test_fake_devices(self):
    self.service._publish_test_data('../testdata/devices')
    eq_(self.service.get_sources(), ["0:13:a2:0:40:89:e5:44", "0:13:a2:0:40:89:e5:43"])

  def test_fake_devices_loop(self):
    for x in range(11): self.service._publish_test_data('../testdata/devices')
    eq_(self.service.get_sources(), ["0:13:a2:0:40:89:e5:44", "0:13:a2:0:40:89:e5:43"])
