
from twisted.internet import task
from collections import defaultdict

class EventListeners():
  def __init__(self):
    self.listeners = defaultdict(list)

  def add(self, event_name, callback):
    self.listeners[event_name].append(callback)

  def notify(self, event_name, data):
    for l in self.listeners[event_name]:
      l(event_name, data)
      yield None 

listeners = EventListeners()

def listen_to(name, callback):
  listeners.add(name, callback);

def fire(name, data={}):
  return task.cooperate(listeners.notify(name, data)).whenDone()
