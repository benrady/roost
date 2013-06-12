from roost.services import web
from nose.tools import * 
from mock import Mock

from twisted.trial import unittest

class TestWeb(unittest.TestCase):
  def test_name(self):
    service = web.Web({})
    eq_(service.name, "web")
