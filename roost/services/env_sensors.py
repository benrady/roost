from twisted.application import service
import roost

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
    reading = {'zone': self.name}
    pin0 = self.read_sample(frame, 'adc-0')
    if pin0:
      reading.update({'temp_f': (pin0 / 10) + self.calibration})
    pin1 = self.read_sample(frame, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    self.setName('env_sensors')
    self.sources = { 
        '\x00\x13\xa2\x00@\x89\xe5C': Source("zone1", -0.82),
        '\x00\x13\xa2\x00@\x89\xe5D': Source("zone2")
    }
    self.properties = {
        "zone1": {"name": "Zone 1"},
        "zone2": {"name": "Zone 2"}
    }

  def on_data(self, event, data):
    packet = data['packet']
    reading = self.sources[packet['source_addr_long']].parse_frame(packet)
    self.properties[reading['zone']].update(reading)

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
