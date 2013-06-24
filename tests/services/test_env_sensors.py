from roost.services.env_sensors import *
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def setUp(self):
    self.service = EnvSensors()
    self.props = self.service.properties
    self.data = {'source': '0:13:a2:0:40:89:e5:43', 'samples':[{'adc-0': 580, 'adc-1': 570}]}

  def test_properties(self):
    eq_(self.props.export(), {"sources": {}})

  def test_new_device(self):
    self.service.on_data('xbee.data', self.data)
    pinout = self.props['sources/0:13:a2:0:40:89:e5:43/pinout']
    eq_(pinout['adc-0'], None)
    eq_(pinout['adc-1'], None)

  def test_existing_device(self):
    self.service.on_data('xbee.data', self.data)
    self.props['sources/0:13:a2:0:40:89:e5:43/pinout/adc-0'] = 'tempF'
    self.service.on_data('xbee.data', self.data)
    eq_(self.props['sources/0:13:a2:0:40:89:e5:43/pinout/adc-0'], 'tempF')

  def test_unconfigured_device(self):
    self.service.on_data('xbee.data', self.data)
    self.service.on_data('xbee.data', self.data)
    assert not self.props['sources/0:13:a2:0:40:89:e5:43/pinout/adc-0']

  @patch('roost.services.env_sensors._now_millis')
  def test_on_data(self, now):
    now.return_value = 1234567890000
    self.service.on_data('xbee.data', self.data)
    self.props['sources/0:13:a2:0:40:89:e5:43/pinout/adc-0'] = 'tempF'
    self.props['sources/0:13:a2:0:40:89:e5:43/pinout/adc-1'] = 'humidity'
    self.service.on_data('xbee.data', self.data)

    reading = self.props['sources/0:13:a2:0:40:89:e5:43/reading']
    eq_(reading['tempF'], 68.03519061583577)
    eq_(reading['humidity'], 49.215754039178876)
    eq_(reading['lastUpdate'], 1234567890000)

  @patch('roost.properties.Properties')
  def test_properties_persisted(self, Prop):
    EnvSensors({'data-dir': 'data'})
    Prop.assert_called_with('data/env_sensors/properties')


