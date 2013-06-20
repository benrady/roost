from twisted.application import service
import time
import roost

def now_millis():
  return int(round(time.time() * 1000))

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    self.setName('env_sensors')
    self.calibration = 0.0
    # FIXME Need a way to assign sources to zones
    self.zones = {
        "zone1": {"name": "Zone 1", "source": '0:13:a2:0:40:89:e5:43'},
        "zone2": {"name": "Zone 2", "source": '0:13:a2:0:40:89:e5:44'}
    }

  def _read_sample(self, samples, pin):
    # XBee analog pins
    # 0 - 1.2v = 0 - 1023
    if samples[0].has_key(pin):
      return 1200 * (samples[0][pin] / 1023.0)

  def _parse_samples(self, samples):
    reading = {'lastUpdate': now_millis()}
    pin0 = self._read_sample(samples, 'adc-0')
    if pin0:
      reading.update({'tempF': (pin0 / 10) + self.calibration})
    pin1 = self._read_sample(samples, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

  def _find_zone(self, source):
    for k, zone in self.zones.items():
      if zone['source'] == source: 
        return zone

  def on_data(self, event, data):
    zone = self._find_zone(data['source'])
    reading = self._parse_samples(data['samples'])
    zone.update(reading)

  def properties(self):
    return {"zones": self.zones}

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
