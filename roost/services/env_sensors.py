from twisted.application import service
import roost

class Source:
  def __init__(self, name, calibration=0.0):
    self.name = name
    self.calibration = calibration

  def read_sample(self, samples, pin):
    # XBee analog pins
    # 0 - 1.2v = 0 - 1023
    if samples[0].has_key(pin):
      return 1200 * (samples[0][pin] / 1023.0)

  def parse_samples(self, samples):
    reading = {'zone': self.name}
    pin0 = self.read_sample(samples, 'adc-0')
    if pin0:
      reading.update({'temp_f': (pin0 / 10) + self.calibration})
    pin1 = self.read_sample(samples, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    self.setName('env_sensors')
    self.sources = { 
        '0:13:a2:0:40:89:e5:43': Source("zone1", -0.82),
        '0:13:a2:0:40:89:e5:44': Source("zone2")
    }
    self.zones = {
        "zone1": {"name": "Zone 1"},
        "zone2": {"name": "Zone 2"}
    }

  def on_data(self, event, data):
    reading = self.sources[data['source']].parse_samples(data['samples'])
    self.zones[reading['zone']].update(reading)

  def properties(self):
    return {"zones": self.zones}

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
