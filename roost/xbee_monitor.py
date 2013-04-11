#!/usr/bin/env python

"""
Continuously read the serial port and process IO data received from a remote XBee.
"""

# Water
# Real: 65.4 / Measured: 68.4 (Vertial Alignment) 3
# Real: 64.7 / Measured: 69.1 (Vertial Alignment) 4.4
# Real: 65.8 / Measured: 69.6 (Vertial Alignment) 3.8
# 3.7

# Air
# Real: 65.3 / Measured: 66.36
# Real: 65.6 / Measured: 68.3

import json, time, sys, os, fcntl

def data_dir():
  return "data"

def now():
  return int(time.time() * 1000)

class Source:
  def __init__(self, name, calibration=0.0):
    self.name = name
    self.calibration = calibration

  def read_sample(self, frame, pin):
    # XBee analog pins
    # 0 - 1.2v = 0 - 1023
    if frame['samples'][0].has_key(pin):
      return 1200 * (frame['samples'][0][pin] / 1023.0)

  def parse_frame(self, frame):
    reading = {'source': self.name, 'timestamp': now()}
    pin0 = self.read_sample(frame, 'adc-0')
    if pin0:
      reading.update({'temp_f': (pin0 / 10) + self.calibration})
    pin1 = self.read_sample(frame, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

sources = { 
    '\x00\x13\xa2\x00@\x89\xe5C': Source("sensor_1", -0.82),
    '\x00\x13\xa2\x00@\x89\xe5D': Source("sensor_2")
}

def get_record(frame):
  source = sources[frame['source_addr_long']]
  return source.parse_frame(frame)

def write_record(record, path):
  out_dir = path + '/temperature/raw'
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)
  time_start = record['timestamp'] - (record['timestamp'] % 3600000)
  with open(out_dir + "/" + str(time_start) + ".lson", "a") as myfile:
    myfile.write(json.dumps(record) + "\n")

def write_to_pipe(record, path):
  fd = False
  try:
    fd = os.open(path + "/temperature/live", os.O_WRONLY | os.O_NONBLOCK)
    os.write(fd, json.dumps(record) + "\n")
  except OSError:
    return None
  finally:
    if (fd):
      os.close(fd)

def read_loop(ser, xbee):
  response = xbee.wait_read_frame()
  record = get_record(response)
  write_record(record, data_dir())
  write_to_pipe(record, data_dir())
