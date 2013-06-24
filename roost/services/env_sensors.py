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
    self.properties = properties.Properties(propfile)
    self.properties['sources'] = {}
    self._pin_types = {
        "tempF": self._read_temp,
        "humidity": self._read_humidity
    }

  def _read_temp(self, pin):
    return {'tempF': (pin / 10)}

  def _read_humidity(self, pin):
    return {'humidity': (pin - 0.22) * 0.073632 }

  def _read_analog_pin(self, pin):
    return 1200 * (pin / 1023.0)

  def _read_pins(self, samples, pinout):
    reading = {'lastUpdate': _now_millis()}
    for sample in samples:
      for pin in sample.keys():
        pin_type = pinout[pin]
        if pin_type:
          volts = self._read_analog_pin(sample[pin])
          reading.update(self._pin_types[pin_type](volts))
    return reading

  def _get_pinout(self, source):
    return self.properties.get_in('sources', source, 'pinout')

  def on_data(self, event, data):
    """Event handler for incoming XBee data"""
    if not data['source'] in self.sources():
      pinout = {}
      for sample in data['samples']:
        for pin in sample.keys():
          pinout[pin] = None
      self.properties.update_in('sources', data['source'], 'pinout', pinout)
    reading = self._read_pins(data['samples'], self._get_pinout(data['source']))
    self.properties.update_in('sources', data['source'], 'reading', reading)

  def pin_types(self):
    """Returns the kinds of readings that can be taken using this service"""
    return self._pin_types.keys()

  def sources(self):
    """Returns the source objects that repesent the sources this service has been notified of"""
    return self.properties['sources']

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
