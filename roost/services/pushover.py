from twisted.application import service
import roost
from roost import properties, httpclient

# https://pushover.net/api
class PushoverService(service.Service):
  def __init__(self, opts={}):
    self.properties = properties.Properties(defaults={'users':[]})

  def _send(self, **kwargs):
    for user in self.properties['users']:
      httpclient.post('https://api.pushover.net/1/messages.json', **dict(kwargs, **{
        'user': user,
        'token': self.properties['token']
        }))

  def send_message(self, msg):
    """Sends a low priority message to all registered devices"""
    self._send(message=msg)

  def send_alert(self, msg):
    """Sends a high priority message to all registered devices"""
    for user in self.properties['users']:
      httpclient.post('https://api.pushover.net/1/messages.json', 
          message=msg,
          user=user,
          token=self.properties['token'], 
          priority=1)

  def set_api_token(self, token):
    self.properties['token'] = token

  def add_user(self, user_id):
    self.properties['users'].append(user_id)

