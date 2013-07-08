
from roost.httpclient import *
from twisted.trial import unittest
from twisted.web import client
from mock import MagicMock, Mock, patch
from StringIO import StringIO


class HttpclientTestCase(unittest.TestCase):
  def setUp(self):
    self.request_patcher = patch.object(client.Agent, 'request')
    self.mock_request = self.request_patcher.start()

  def tearDown(self):
    self.request_patcher.stop()

  def assert_body(self, url, expected_body):
    self.assertEquals(self.mock_request.call_args[0], ('POST', url))
    kwargs = self.mock_request.call_args[1]
    stringIO = StringIO()
    kwargs['bodyProducer'].startProducing(stringIO)
    self.assertEquals(stringIO.getvalue(), expected_body)

  def test_post_with_body(self):
    post('http://localhost', "this is the body")
    self.assert_body('http://localhost', 'this is the body')

  def test_post_with_keywords(self):
    post('http://localhost', value1='one', value2='two')
    self.assert_body('http://localhost', "value2=two&value1=one")
