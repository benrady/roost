
import os, time, whisper

class Storage():
  def __init__(self, data_dir, service_name):
    self.root_path = data_dir + '/' + service_name

  def _get_path(self, key):
    return self.root_path + '/' + key

  def write(self, key, value):
    path = self._get_path(key)
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
      os.makedirs(parent)
      whisper.create(path, [(3600, 604800)])
    whisper.update(path, value, time.time())

  def fetch(self, key, since, until):
    return whisper.fetch(self._get_path(key), since, until)
