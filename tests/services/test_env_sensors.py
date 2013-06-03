from roost.services import env_sensors
from nose.tools import * 
from mock import Mock

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def test_on_data(self):
    service = env_sensors.EnvSensors()
    service.on_data('xbee.data', {"packet": {}})
