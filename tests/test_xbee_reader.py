from roost import xbee_reader, events
from nose.tools import * 
from mock import Mock

import types, unittest, shutil, os

class TestXBeeReader(unittest.TestCase):

  def setUp(self):
    self.reader = xbee_reader.XBeeReader()

  def test_handle_packet(self):
    events.fire = Mock()
    packet1 = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 605}], 'options': '\x01'} 
    packet2 = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5D', 'source_addr': 'r\xda', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 601, 'adc-1': 570}], 'options': '\x01'}
    self.reader.handle_packet(packet1)
    events.fire.assert_called_with('xbee.data', {"packet": packet1})
    
