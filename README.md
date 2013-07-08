# Roost -- Open Source Home Automation

Roost is open-source home automation based on the Raspberry Pi

## Supported Devices

The following devices/services are supported in the latest release

* Local Weather Reports (via Weather Underground)
* Push notifications (via Pushover)

Roost is an open system (both software and hardware), so you can always make your own devices using ZigBee compatible radios, or write your own Roost "service" in Python to connect Roost to a new device. 

### 3rd Party Peripherals

[ZigBee certified products](http://www.zigbee.org/Products/ByFunction/AllFunctions.aspx)

## Recommended Hardware

Roost uses a Raspberry Pi Model B as a base station, and talks to devices in your home using a mesh radio network, so there are no wires to run. A complete parts list for a base station [will be available](https://docs.google.com/spreadsheet/ccc?key=0Ann48md_Q6mkdGxOWUYwYnFqajRUcWVmSHZIcS0xV3c#gid=0).

## Releases

Roost is currently under development. Roost is expected to be released as a debian package (for easy setup on the Raspberry Pi). No stable releases are currently available. Feedback and pull requests are encouraged.

## Installation

####Install dependencies

`sudo apt-get install python-setuptools python-twisted`

####Clone this repository; Run installation

`sudo python setup.py install`

## Support

Telnet access

## Development

Roost is primarily test driven. You can run the tests with [trial](https://twistedmatrix.com/trac/wiki/TwistedTrial).

You can run a development server like so: `twistd -n roost`
