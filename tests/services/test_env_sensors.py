from roost.services import env_sensors
from nose.tools import * 
from mock import Mock

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def setUp(self):
    self.service = env_sensors.EnvSensors()

  def test_test_zones(self):
    eq_(self.service.properties()['zones'], {
      'zone1': {"name": "Zone 1"},
      'zone2': {"name": "Zone 2"}
    })

  def test_on_data(self):
    data = {'source': '0:13:a2:0:40:89:e5:43', 'samples':[{'adc-0': 580, 'adc-1': 570}]}
    self.service.on_data('xbee.data', data)
    zones = self.service.properties()['zones']
    eq_(zones['zone1']['temp_f'], 67.21519061583578)
    eq_(zones['zone1']['humidity'], 49.215754039178876)
