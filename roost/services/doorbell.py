from twisted.application import service
import time
import roost
from roost import properties, storage

class Doorbell(service.Service):
  def __init__(self):
    super(Doorbell, self).__init__(*args, **kwds)
    self.last_notification = None

  def on_data(self, event, data):
    if any([s.get('ddc-0', False) for s in data['samples']]):
      if not self.last_notification or time.time() - self.last_notification > 10:
        roost.notify('Doorbell')
        self.last_notification = time.time()

  def startService(self):
    roost.listen_to('xbee.data', self.on_data)
    service.Service.startService(self)
