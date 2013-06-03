from roost import services
from nose.tools import * 
from mock import Mock
from twisted.trial import unittest

class TestMain(unittest.TestCase):
  def test_load_services(self):
    services._services = []
    #services.start({})
    #eq_(len(services._services), 1)
    # FIXME
