"""
Roost module
"""

import events, services

listen_to = events.listen_to
fire_event = events.fire
add_service = services.add
find_service = services.find

def notify(message):
  s = find_service('pushover')
  s.send_message(message)
