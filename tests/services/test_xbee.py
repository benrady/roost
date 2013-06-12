from roost.services import xbee
from roost import events
from nose.tools import * 
from mock import Mock

import types, unittest, shutil, os

class TestXBeeReader(unittest.TestCase):

  def setUp(self):
    self.reader = xbee.XBeeReader()
    self.packet1 = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 605}], 'options': '\x01'} 
    self.packet2 = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5D', 'source_addr': 'r\xda', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 601, 'adc-1': 570}], 'options': '\x01'}
    events.fire = Mock()

  def test_handle_packet(self):
    self.reader.handle_packet(self.packet1)
    events.fire.assert_called_with('xbee.data', {"packet": self.packet1})

  def test_new_source(self):
    self.reader.handle_packet(self.packet1)
    events.fire.assert_any_call('xbee.source.new', {
      "source": self.packet1['source_addr_long'],
      "packet": self.packet1
    })
    eq_(self.reader.sources, set([self.packet1['source_addr_long']]))

  def test_existing_source(self):
    self.reader.handle_packet(self.packet1)
    self.reader.handle_packet(self.packet1)
    eq_(events.fire.call_count, 3) # Would be four times if the source weren't new



class TestXBeeService(unittest.TestCase):
  def setUp(self):
    self.service = xbee.XBeeService()

  def test_no_sources_by_default(self):
    eq_(self.service.get_sources(), set())
