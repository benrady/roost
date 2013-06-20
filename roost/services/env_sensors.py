from twisted.application import service
import time
import roost

def now_millis():
  return int(round(time.time() * 1000))

class Source:
  def __init__(self, zone, calibration=0.0):
    self.zone = zone
    self.calibration = calibration

  def read_sample(self, samples, pin):
    # XBee analog pins
    # 0 - 1.2v = 0 - 1023
    if samples[0].has_key(pin):
      return 1200 * (samples[0][pin] / 1023.0)

  def parse_samples(self, samples):
    reading = {'lastUpdate': now_millis()}
    pin0 = self.read_sample(samples, 'adc-0')
    if pin0:
      reading.update({'tempF': (pin0 / 10) + self.calibration})
    pin1 = self.read_sample(samples, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    self.setName('env_sensors')
    # FIXME Need a way to assign sources to zones
    self.sources = { 
        '0:13:a2:0:40:89:e5:43': Source("zone1", -2.5),
        '0:13:a2:0:40:89:e5:44': Source("zone2")
    }
    self.zones = {
        "zone1": {"name": "Zone 1"},
        "zone2": {"name": "Zone 2"}
    }

  def on_data(self, event, data):
    source = self.sources[data['source']]
    reading = source.parse_samples(data['samples'])
    self.zones[source.zone].update(reading)

  def properties(self):
    return {"zones": self.zones}

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
