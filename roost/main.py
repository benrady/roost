"""
This module contains Roost's `main` method. `main` is executed as the command line ``roost`` program.
"""
from xbee import ZigBee
import sys, serial

from xbee_monitor import read_loop

def main(device='/dev/ttyUSB0'):
  print 'Starting Roost. Connecting to ' + device
  ser = serial.Serial(device, 9600)
  xbee = ZigBee(ser, escaped=True)
  while True:
    try:
      read_loop(ser, xbee)
    except KeyboardInterrupt:
        break
  ser.close()
  sys.exit(0)

if __name__ == "__main__":
  main(*sys.argv[1:])
