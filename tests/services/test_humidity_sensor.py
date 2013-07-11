from roost.services.humidity_sensor import *
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestHumiditySensor(unittest.TestCase):
  def setUp(self):
    self.service = HumiditySensor()
    self.props = self.service.properties
    self.data = {'source': '0:13:a2:0:40:89:e5:43', 'samples':[{'adc-0': 580, 'adc-1': 570}]}
    self.props['sources'].append('0:13:a2:0:40:89:e5:43')

  def test_properties(self):
    eq_(self.props.export(), {"sources": ['0:13:a2:0:40:89:e5:43'], 'pin': 'adc-1'})

  @patch('roost.services.humidity_sensor._now_millis')
  def test_on_data(self, now):
    now.return_value = 1234567890000
    self.service.on_data('xbee.data', self.data)
    reading = self.props['sources/0:13:a2:0:40:89:e5:43/reading']
    eq_(reading['humidity'], 49.215754039178876)
    eq_(reading['lastUpdate'], 1234567890000)

  @patch('roost.properties.Properties')
  def test_properties_persisted(self, Prop):
    HumiditySensor({'data-dir': 'data'})
    Prop.assert_called_with('data/humidity_sensor/properties', defaults={
      'sources': [],
      'pin': 'adc-1'
    })


