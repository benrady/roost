from roost import xbee_monitor 
from nose.tools import * 

import types, unittest, shutil, os

mark1_frame = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5C', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 599}], 'options': '\x01'}
mark2_frame = {'source_addr_long': '\x00\x13\xa2\x00@\x89\xe5D', 'source_addr': '\x92u', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 599, 'adc-1': 350}], 'options': '\x01'}

def now():
  return 1234567890000

xbee_monitor.now = now # Fake implemention of now

def test_parse_frame():
  reading = xbee_monitor.get_record(mark2_frame)
  eq_(reading['source'], 'sensor_2')
  eq_(reading['humidity'], 30.21394758756598)
  eq_(reading['temp_f'], 70.26392961876833)
  eq_(reading['timestamp'], 1234567890000)

def test_parse_frame_without_humidity():
  reading = xbee_monitor.get_record(mark1_frame)
  eq_(reading['source'], 'sensor_1')
  eq_(reading['temp_f'], 69.44392961876834)
  eq_(reading['timestamp'], 1234567890000)

