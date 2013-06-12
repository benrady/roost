from roost import services
from nose.tools import * 
from mock import Mock
from twisted.trial import unittest

class TestMain(unittest.TestCase):

  def test_start(self):
    serviceClass = services.env_sensors.EnvSensors
    app = Mock()
    services._services = [serviceClass]
    services.start(app, {})
    assert isinstance(services.find('env_sensors'), serviceClass)
