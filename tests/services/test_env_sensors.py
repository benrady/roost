from roost.services import env_sensors
from nose.tools import * 
from mock import Mock

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def setUp(self):
    self.service = env_sensors.EnvSensors()

  def test_test_zones(self):
    eq_(self.service.properties['zone1'], {"name": "Zone 1"})

  def test_on_data(self):
    packet = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5D', 'source_addr': 'r\xda', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 580, 'adc-1': 570}], 'options': '\x01'}
    self.service.on_data('xbee.data', {"packet": packet})
    eq_(self.service.properties['zone2']['temp_f'], 68.03519061583577)
    eq_(self.service.properties['zone2']['humidity'], 49.215754039178876)
