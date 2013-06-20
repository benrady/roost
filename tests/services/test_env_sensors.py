from roost.services import env_sensors
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def setUp(self):
    self.service = env_sensors.EnvSensors()
    self.data = {'source': '0:13:a2:0:40:89:e5:43', 'samples':[{'adc-0': 580, 'adc-1': 570}]}

  def test_test_zones(self):
    eq_(self.service.properties()['zones'], {
        "zone1": {"name": "Zone 1", "source": '0:13:a2:0:40:89:e5:43'},
        "zone2": {"name": "Zone 2", "source": '0:13:a2:0:40:89:e5:44'}
    })

  @patch('roost.services.env_sensors.now_millis')
  def test_on_data(self, now):
    now.return_value = 1234567890000
    self.service.on_data('xbee.data', self.data)
    zones = self.service.properties()['zones']
    eq_(zones['zone1']['tempF'], 68.03519061583577)
    eq_(zones['zone1']['humidity'], 49.215754039178876)
    eq_(zones['zone1']['lastUpdate'], 1234567890000)
