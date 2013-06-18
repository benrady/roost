from roost import storage
from nose.tools import * 
from mock import Mock, patch
from twisted.trial import unittest

import time, os

class TestStorage(unittest.TestCase):
  def setUp(self):
    self.storage = storage.Storage('temp_data', 'service_name')

  @patch('whisper.update')
  @patch('whisper.create')
  def test_create_on_new(self, create, update):
    self.storage.write('foo/bar/baz', 1.0)
    create.assert_called_with('temp_data/service_name/foo/bar/baz', [(3600, 604800)])

  @patch('whisper.update')
  @patch('whisper.create')
  @patch('time.time')
  def test_write(self, time, create, update):
    time.return_value = 1234567890
    self.storage.write('foo/bar/baz', 1.0)
    update.assert_called_with('temp_data/service_name/foo/bar/baz', 1.0, 1234567890) 

  @patch('whisper.fetch')
  def test_read(self, fetch):
    self.storage.fetch('foo/bar/baz', 1000, 2000)
    fetch.assert_called_with('temp_data/service_name/foo/bar/baz', 1000, 2000)
