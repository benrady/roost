#!/usr/bin/env python

# Python setup script
# http://docs.python.org/2/distutils/setupscript.html

from setuptools import setup, find_packages

long_description = """
Similar to the Nest thermostat, Roost adapts to your habits and figures out an optimal schedule for heat, A/C, and humidity controls.

Unlike the Nest, Roost is built around open standards and easy data access. It provides an API for data access and control and can be assembled from open-source software and hardware.
"""

import sys

try:
    import twisted
except ImportError:
    raise SystemExit("twisted not found.  Make sure you "
                     "have installed the Twisted core package.")
def refresh_plugin_cache():
    from twisted.plugin import IPlugin, getPlugins
    list(getPlugins(IPlugin))

setup(name='Roost',
      version='0.1',
      description='Open-Source Adaptive Thermostat and Home Automation',
      long_description=long_description,
      author='Ben Rady',
      author_email='benrady@gmail.com',
      packages=find_packages(),
      install_requires=['txXBee>=0.0.4', 'twisted>=12.0.0'],
      url='http://github.com/benrady/roost',
      package_data={
          'twisted': ['plugins/twist_plugin.py'],
          'web': ['public/**']
      },
      data_files=[
        ('/etc/init.d', ['deb/init.d/roost']),
        ('/etc/roost', ['deb/roost.conf'])
      ])

refresh_plugin_cache()
