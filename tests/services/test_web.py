import roost.services
from roost.services import web
from nose.tools import * 
from mock import Mock, patch
import json

from twisted.internet.defer import succeed
from twisted.trial import unittest
from twisted.web.test.test_web import DummyRequest

class TestWeb(unittest.TestCase):
  def test_name(self):
    service = web.Web({'port': '80', 'web-dir': 'web/public'})
    eq_(service.name, "web")

def _render(resource, request):
  result = resource.render(request)
  if isinstance(result, str):
    request.write(result)
    request.finish()
    return succeed(None)
  elif result is twisted.web.server.NOT_DONE_YET:
    if request.finished:
      return succeed(None)
    else:
      return request.notifyFinish()
  else:
    raise ValueError("Unexpected return value: %r" % (result,))

class TestServiceResource(unittest.TestCase):

  @patch('roost.services.find')
  def test_get_properties(self, find):
    service = Mock()
    service.name = 'web'
    service.properties = Mock()
    props = {"prop1": 1}
    service.properties.return_value = props
    find.return_value = service
    r = web.ServiceResource()
    request = DummyRequest(['web', 'properties'])
    d = _render(r, request)
    def rendered(ignored):
      self.assertEquals(request.responseCode, None) # Gets treated as 200 OK
      self.assertEquals(json.loads("".join(request.written)), props)
    d.addCallback(rendered)
    return d
