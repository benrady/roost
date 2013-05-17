#!/usr/bin/env python

# Python setup script
# http://docs.python.org/2/distutils/setupscript.html

from setuptools import setup, find_packages

long_description = """
Similar to the Nest thermostat, Roost adapts to your habits and figures out an optimal schedule for heat, A/C, and humidity controls.

Unlike the Nest, Roost is built around open standards and easy data access. It provides an API for data access and control and can be assembled from open-source software and hardware.
"""

setup(name='Roost',
      version='0.1',
      description='Open-Source Adaptive Thermostat and Home Automation',
      long_description=long_description,
      author='Ben Rady',
      author_email='benrady@gmail.com',
      packages=find_packages(),
      #install_requires=['XBee>=2.0.0', 'pyserial>=2.6'],  pulled into this project
      url='http://github.com/benrady/roost',
      entry_points={
        'console_scripts': [
        'roost = roost.main:main',
        ]
      },
      data_files=[
        ('/var/roost/www', ['web/public']),
        ('/etc/roost', ['conf/roost.conf']),
        ('/etc/init.d', ['bin/roost.sh'])
      ]
     )
