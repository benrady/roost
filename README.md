# About Roost
Roost is an open-source adaptive thermostat.

Similar to the [Nest](http://www.nest.com/) thermostat, Roost adapts to your habits and figures out an optimal schedule for heat, A/C, and humidity controls.

Unlike the Nest, Roost is built around open standards and easy data access. Roost does not rely on any external services. It provides an API for data access and control and can be assembled from open-source software and hardware for under $200.

## Software

Roost will provide simple APIs, making integration with other devices and software easy.

## Recommended Hardware

Roost uses a Raspberry Pi Model B as a base station, and talks to environmental sensors using a mesh radio network, so there are no wires to run through your walls. A complete parts lists (with vendors) [will be available](https://docs.google.com/spreadsheet/ccc?key=0Ann48md_Q6mkdGxOWUYwYnFqajRUcWVmSHZIcS0xV3c#gid=0).

The current hardware setup emphasizes ease of setup and flexibility over efficiency and cost, but alternate setups are greatly encouraged. Every reasonable accommodation will be made for other types of hardware.

## Releases

Roost is currently under development. Roost is expected to be released as a debian package (for easy setup on the Raspberry Pi). No stable releases are currently available. Feedback and pull requests are encouraged.

## Development

Roost is primarily test driven. A great way to run tests is with `tdaemon -t nose .`
