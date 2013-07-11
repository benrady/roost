from twisted.application import service
import time
import roost
from roost import properties

def _now_millis():
  return int(round(time.time() * 1000))

class HumiditySensor(service.Service):
  def __init__(self, opts={}):
    self.setName('humidity_sensor')
    propfile = None
    if opts.has_key('data-dir'):
      propfile = opts.get('data-dir') + '/' + self.name + '/properties'
    self.properties = properties.Properties(propfile, defaults={
      'sources': [],
      'pin': 'adc-1'
    })

  def _read_humidity(self, pin):
    return {'humidity': (pin - 0.22) * 0.073632 }

  def _read_analog_pin(self, pin):
    return 1200 * (pin / 1023.0)

  def _read_pins(self, samples):
    reading = {'lastUpdate': _now_millis()}
    for sample in samples:
      volts = self._read_analog_pin(sample[self.properties['pin']])
      reading.update(self._read_humidity(volts))
    return reading

  def on_data(self, event, data):
    """Event handler for incoming XBee data"""
    reading = self._read_pins(data['samples'])
    self.properties.update_in('sources', data['source'], 'reading', reading)

  def sources(self):
    """Returns the source objects that repesent the sources this service has been notified of"""
    return self.properties['sources']

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(HumiditySensor)
