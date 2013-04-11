"""
This module contains Roost's `main` method. `main` is executed as the command line ``roost`` program.
"""
import sys

from xbee_monitor import read_loop

def main():
  print 'Starting Roost'
  ser = serial.Serial('/dev/ttyUSB0', 9600)
  xbee = ZigBee(ser, escaped=True)
  while True:
    try:
      read_loop(ser, xbee)
    except KeyboardInterrupt:
        break
  ser.close()
  sys.exit(0)
