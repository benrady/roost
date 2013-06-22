from twisted.application import service
import time
import roost
from roost import properties, storage

def _now_millis():
  return int(round(time.time() * 1000))

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    self.setName('env_sensors')
    propfile = None
    if opts.has_key('data-dir'):
      self.storage = storage.Storage(opts.get('data-dir'), self.name)
      propfile = opts.get('data-dir') + '/env_sensors/properties'
    self.calibration = 0.0
    self.properties = properties.Properties(propfile)
    self.properties['zones/zone1/name'] = 'Zone 1'
    self.properties['zones/zone2/name'] = 'Zone 2'

  def _read_sample(self, samples, pin):
    # XBee analog pins
    # 0 - 1.2v = 0 - 1023
    if samples[0].has_key(pin):
      return 1200 * (samples[0][pin] / 1023.0)

  def _parse_samples(self, samples):
    reading = {'lastUpdate': _now_millis()}
    pin0 = self._read_sample(samples, 'adc-0')
    if pin0:
      reading.update({'tempF': (pin0 / 10) + self.calibration})
    pin1 = self._read_sample(samples, 'adc-1')
    if pin1: 
      reading.update({'humidity': (pin1 - 0.22) * 0.073632 })
    return reading

  def on_data(self, event, data):
    zone = self.properties.get_in('sources', data['source'])
    reading = self._parse_samples(data['samples'])
    self.properties.update_in('zones', zone, reading)

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
