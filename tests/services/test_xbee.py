from roost.services.xbee import *
from roost import events
from nose.tools import * 
from mock import Mock, patch

import types, unittest, shutil, os

class TestXBeeReader(unittest.TestCase):

  def setUp(self):
    self.reader = XBeeReader()
    self.reader.on_packet = Mock()
    self.packet_samples = [{'adc-0': 605, 'adc-1': 570}]
    self.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': self.packet_samples, 'options': '\x01'} 

  def test_handle_packet(self):
    self.reader.handle_packet(self.packet)
    self.reader.on_packet.assert_called_with(self.packet)

  @patch('roost.events.fire')
  def test_no_samples(self, fire):
    packet = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C'} 
    self.reader.handle_packet(packet)
    fire.assert_not_called()


class TestXBeeService(unittest.TestCase):
  def setUp(self):
    self.service = XBeeService()
    self.packet_samples = [{'adc-0': 605, 'adc-1': 570}]
    self.packet = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': self.packet_samples, 'options': '\x01'} 
    self.source = '0:13:a2:0:40:89:e5:43'

  def test_no_sources_by_default(self):
    eq_(self.service.get_sources(), {})

  @patch('roost.events.fire')
  def test_new_source(self, fire):
    self.service._on_packet(self.packet)
    fire.assert_any_call('xbee.source.new', {
      "source": '0:13:a2:0:40:89:e5:43',
      "samples": self.packet_samples
    })
    eq_(self.service.get_sources(), {self.source: {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u'}})

  @patch('roost.events.fire')
  def test_existing_source(self, fire):
    self.service._on_packet(self.packet)
    self.service._on_packet(self.packet)
    eq_(fire.call_count, 3) # Would be four times if the source weren't new

  def test_properties(self):
    eq_(self.service.properties.export(), {'sources': {}})

  def test_fake_devices(self):
    self.service._publish_test_data('../testdata/devices')
    eq_(self.service.get_sources().keys(), ["0:13:a2:0:40:89:e5:44", "0:13:a2:0:40:89:e5:43"])

  def test_fake_devices_loop(self):
    for x in range(11): self.service._publish_test_data('../testdata/devices')
    eq_(self.service.get_sources().keys(), ["0:13:a2:0:40:89:e5:44", "0:13:a2:0:40:89:e5:43"])

  @patch('twisted.internet.reactor.callFromThread')
  def test_send_at_command(self, call):
    self.service._on_packet(self.packet)
    self.service.reader.send = Mock()
    self.service.send_at_command("0:13:a2:0:40:89:e5:43", "ID")
    call.assert_called_with(self.service.reader.send, 
        'remote_at', 
        dest_addr_long='\x00\x13\xa2\x00@\x89\xe5C',
        dest_addr='\x92u',
        command='ID')

  #Message from a new device when bringing pin 0 high
  # {'source_addr_long': '\x00\x13\xa2\x00@\xa2X\xa4', 'source_addr': '\xe3\xf2', 'parent_source_addr': '\xff\xfe', 'digi_profile_id': '\xc1\x05', 'options': '\x02', 'sender_addr': '\xe3\xf2', 'source_event': '\x01', 'node_id': ' ', 'device_type': '\x01', 'manufacturer_id': '\x10\x1e', 'sender_addr_long': '\x00\x13\xa2\x00@\xa2X\xa4', 'id': 'node_id_indicator'}

