
from roost import events
from nose.tools import * 
from twisted.trial import unittest
from mock import Mock

from twisted.internet import task

class TestEventsListeners(unittest.TestCase):
  def setUp(self):
    self.listeners = events.EventListeners()

  def test_add_listener(self):
    mock = Mock()
    self.listeners.add('test', mock)
    iterator = self.listeners.notify('test', 'hello world')
    task.cooperate(iterator).whenDone().addCallback(lambda i: mock.assert_called_with( 'test', 'hello world'))

  def test_listen_and_fire(self):
    mock = Mock()
    events.listen_to('test', mock)
    d = events.fire('test', 'hello world')
    d.addCallback(lambda i: mock.assert_called_with('test', 'hello world'))
    return d
