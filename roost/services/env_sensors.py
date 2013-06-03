from twisted.application import service
import roost

class EnvSensors(service.Service):
  def __init__(self, opts={}):
    None

  def on_data(self, event, data):
    print data

  def startService(self):
    service.Service.startService(self)
    roost.listen_to('xbee.data', self.on_data)

roost.add_service(EnvSensors)
