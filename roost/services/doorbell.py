from twisted.application import service
import time
import roost
from roost import properties, storage

class DoorbellService(service.Service):
  def __init__(self):
    self.last_notification = None
    self.setName('doorbell')

  def on_data(self, event, data):
    if any([s.get('dio-0', False) for s in data['samples']]):
      if not self.last_notification or time.time() - self.last_notification > 10:
        roost.notify('Doorbell')
        self.last_notification = time.time()

  def startService(self):
    roost.listen_to('xbee.data', self.on_data)
    service.Service.startService(self)

roost.add_service(DoorbellService)
