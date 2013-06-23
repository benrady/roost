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
    self.p['zones/zone2/name'] = 'two'
    self.p['zones/zone2/bitflags'] = [1, 2, 8]
    eq_(self.p['zones/zone2/name'], 'two')
    eq_(self.p['zones'], {"zone2": {'name': 'two', 'bitflags': [1, 2, 8]}})

  def test_missing_keys(self):
    eq_(self.p['missing'], {})

  def test_incompatible_values_are_overwritten(self):
    self.p['zones'] = 'foo'
    self.p['zones/zone2'] = 'two'
    eq_(self.p['zones'], {'zone2': 'two'})

    self.p['zones/zone2/a/b/c'] = 'd'
    eq_(self.p['zones'], {'zone2': {'a': {'b': {'c': 'd'}}}})

  def test_maps_are_merged(self):
    self.p['zones/zone2'] = 'two'
    self.p['zones'] = {'zone1': 'one'}
    eq_(self.p['zones'], {'zone2': 'two', 'zone1': 'one'})

  def test_creates_keys_for_submaps(self):
    self.p['zones'] = {'zone1': {'name': 'one'}}
    self.p['zones/zone1/device/addr'] = 'abc123'
    eq_(self.p['zones/zone1/device/addr'], 'abc123')

  def test_export(self):
    self.p['devices'] = ["a", "b", "c"]
    self.p['zones/zone2'] = 'two'
    self.p['zones/zone1'] = 1
    eq_(self.p.export(), {
      'zones': {'zone1': 1, 'zone2': 'two'}, 
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

  def test_save(self):
    p = properties.Properties('data/test')
    p['foo'] = 'bar'
    p = properties.Properties('data/test')
    eq_(p['foo'], 'bar')

  def test_default_properties(self):
    p = properties.Properties(defaults={'foo': 'bar'})
    eq_(p.export(), {'foo':'bar'})


