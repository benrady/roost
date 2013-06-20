from roost import properties
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

class TestProperies(unittest.TestCase):
  def setUp(self):
    self.p = properties.Properties()

  def test_export(self):
    self.p['things'] = {'thing2': 'two'}
    eq_(self.p.export({"things" : {'thing1': 1}}), {'things': {'thing1': 1, 'thing2': 'two'}})

  def test_save(self):
    self.p.save('things/thing2', 'two')
    eq_(self.p.export({}), {'things': {'thing2': 'two'}})

