from roost.services.pushover import *
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestEnvSensors(unittest.TestCase):
  def setUp(self):
    self.service = PushoverService()
    self.service.set_api_token('abc123')
    self.service.add_user('foobar')

  def assert_post(self, post, **kwargs):
    post.assert_called_with('https://api.pushover.net/1/messages.json', **kwargs)

  def test_start(self):
    self.service.startService()
    assert self.service.running
    eq_(self.service.name, "pushover")

  @patch('roost.httpclient.post')
  def test_send_message(self, post):
    self.service.send_message("hello world")
    self.assert_post(post, message='hello world', token='abc123', user='foobar')

  # Maybe this should just listen to events and re-publish them to pushover, rather
  # than being directly invoked by services?

