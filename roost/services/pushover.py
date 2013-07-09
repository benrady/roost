from twisted.application import service
import roost
from roost import properties, httpclient

# https://pushover.net/api
class PushoverService(service.Service):
  def __init__(self, opts={}):
    self.setName('pushover')

    # FIXME Duplicated in env_sensors.py
    propfile = None
    if opts.has_key('data-dir'):
      propfile = opts.get('data-dir') + '/' + self.name + '/properties'
    self.properties = properties.Properties(propfile, defaults={'users':[]})

  def _send(self, message, opts):
    for user in self.properties['users']:
      httpclient.post('https://api.pushover.net/1/messages.json', **dict(opts, **{
        'user': user,
        'message': message,
        'token': self.properties['token']
        }))

  def send_message(self, msg, opts={}):
    """Sends a low priority message to all registered devices"""
    self._send(msg, opts)

  def set_api_token(self, token):
    self.properties['token'] = token

  def add_user(self, user_id):
    self.properties['users'].append(user_id)

roost.add_service(PushoverService)
