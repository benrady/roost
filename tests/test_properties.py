from roost import properties
from nose.tools import * 
from mock import Mock, patch

from twisted.trial import unittest

# Properties should be written to disk on save and loaded on creation
# Each property is referred to by a heirarchial path
# They can be alpha or numeric
# The can optionally be persisted
class TestProperies(unittest.TestCase):
  def setUp(self):
    self.p = properties.Properties()

  def test_heirarchy(self):
    self.p['zones/zone2'] = 'two'
    eq_(self.p['zones/zone2'], 'two')
    eq_(self.p['zones'], {"zone2": 'two'})

  def test_missing_keys(self):
    eq_(self.p['missing'], None)

  def test_values_at_every_level(self):
    self.p['zones/zone2'] = 'two'
    self.p['zones'] = 'foo'
    eq_(self.p['zones/zone2'], 'two')

  def test_export(self):
    self.p['devices'] = ["a", "b", "c"]
    self.p['zones/zone2'] = 'two'
    self.p['zones/zone1'] = 1
    self.p['zones'] = 'foo' # You'd never really want to do this, but you can
    eq_(self.p.export(), {
      'zones': {'zone1': 1, 'zone2': 'two', 'foo': None}, 
      'devices': ["a", "b", "c"]})
  
  def test_set(self):
    self.p['zones/zone1/temp'] = 'one'
    self.p['zones/zone1'] = {'temp' : 1, 'calibration': 2}
    eq_(self.p['zones/zone1/temp'], 1)
    eq_(self.p['zones/zone1/calibration'], 2)

  def test_update_in(self):
    self.p.update_in('zones', 'zone1', {'temp': 1})
    self.p.update_in('zones', 'zone2', 'temp', 2)
    self.p.update_in('sources', 'ab:cd')
    eq_(self.p['zones/zone1/temp'], 1)
    eq_(self.p['zones/zone2/temp'], 2)
    eq_(self.p['sources'], 'ab:cd')

