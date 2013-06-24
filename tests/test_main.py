from roost.main import *
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestMain(unittest.TestCase):
  @patch('roost.find_service')
  def test_make_service(self, find):
    return makeService({
      'xbee_device': 'testdata/devices',
      'port': '8080',
      'telnet-users': 'deb/users.txt',
      'data-dir': 'data',
      'web-dir': 'web/public',
    })
