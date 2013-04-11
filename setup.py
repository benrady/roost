#!/usr/bin/env python

from distutils.core import setup

setup(name='Roost',
      version='0.1',
      description='Open-Source Adaptive Thermostat',
      author='Ben Rady',
      author_email='benrady@gmail.com',
      url='github.com/benrady/roost',
      packages=['distutils', 'distutils.command'],
      requires=['xbee', 'pyserial'])
