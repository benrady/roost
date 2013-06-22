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
    eq_(self.props.export(), {
      "zones": {
        "zone1": {"name": "Zone 1"},
        "zone2": {"name": "Zone 2"}
      } 
    })

  @patch('roost.services.env_sensors._now_millis')
  def test_on_data(self, now):
    self.props['sources/0:13:a2:0:40:89:e5:43'] = 'zone1'
    now.return_value = 1234567890000
    self.service.on_data('xbee.data', self.data)
    eq_(self.props['zones/zone1/tempF'], 68.03519061583577)
    eq_(self.props['zones/zone1/humidity'], 49.215754039178876)
    eq_(self.props['zones/zone1/lastUpdate'], 1234567890000)

  def test_unknown_device(self):
    self.props['sources/0:13:a2:0:40:89:e5:43'] = 'zone2'
    self.service.on_data('xbee.data', self.data)
    assert not self.props['zones/zone1/tempF']

  @patch('roost.properties.Properties')
  def test_properties_persisted(self, Prop):
    EnvSensors({'data-dir': 'data'})
    Prop.assert_called_with('data/env_sensors/properties')


