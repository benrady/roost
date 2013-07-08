from roost.services.doorbell import *
from roost import events
from nose.tools import * 
from mock import Mock, patch

import types, unittest, shutil, os, time

class TestDoorbellService(unittest.TestCase):

  def setUp(self):
    self.service = Doorbell()
    self.packet_samples = [{'ddc-0': True}]
    self.data = {'source': '0:13:a2:0:40:89:e5:43', 'source_addr': '0F', 'samples': self.packet_samples} 

  @patch('roost.listen_to')
  def test_start_service(self, listen_to):
    self.service.startService()
    assert self.service.running
    listen_to.assert_called_with('xbee.data', self.service.on_data)

  @patch('roost.notify')
  def test_send_on_true_sample(self, notify):
    self.service.on_data('xbee.data', self.data)
    notify.assert_called_with('Doorbell')

  @patch('roost.notify')
  def test_no_send_on_false_sample(self, notify):
    self.data['samples'] = [{'ddc-0': False}]
    self.service.on_data('xbee.data', self.data)
    assert not notify.called

  @patch('roost.notify')
  def test_send_on_true_sample(self, notify):
    self.service.on_data('xbee.data', self.data)
    notify.assert_called_with('Doorbell')

  @patch('roost.notify')
  def test_debounce(self, notify):
    self.service.on_data('xbee.data', self.data)
    self.service.on_data('xbee.data', self.data)
    eq_(notify.call_count, 1)

  @patch('time.time')
  @patch('roost.notify')
  def test_no_debounce_after_10_seconds(self, notify, time):
    time.return_value = 0
    self.service.on_data('xbee.data', self.data)
    time.return_value = 11
    self.service.on_data('xbee.data', self.data)
    eq_(notify.call_count, 2)

