from roost import server 
from nose.tools import * 
from tornado.testing import AsyncHTTPTestCase

class TestServer(AsyncHTTPTestCase):
  def get_app(self):
    return server.application

  def test_homepage(self):
    response = self.fetch('/')
    eq_("Hello, world", response.body)
