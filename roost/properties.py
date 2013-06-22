import copy, os, pickle

def _dict_merge(a, b):
  if not isinstance(b, dict) or  not isinstance(a, dict):
    return b
  result = copy.deepcopy(a)
  for k, v in b.iteritems():
    if k in result and isinstance(result[k], dict):
      result[k] = _dict_merge(result[k], v)
    else:
      result[k] = copy.deepcopy(v)
  return result 

def _expand_dict(d, keylist):
  for k in keylist[:-1]:
    if k not in d or not isinstance(d[k], dict):
      d[k] = {} 
    d = d[k]
  return d

class Properties():

  def __init__(self, save_path=None):
    self._dict = {}
    self.save_path = save_path
    if self.save_path:
      if os.path.exists(self.save_path):
        with open(self.save_path) as f:
          self._dict = pickle.load(f)

  def __getitem__(self, subkey):
    keylist = subkey.split('/')
    d = self._dict
    for k in keylist[:-1]:
      d = d[k]
    return d.get(keylist[-1], {})

  def __setitem__(self, subkey, value):
    '''Set a value, merging keys and values in a dict onto a subkey in the properties'''
    keylist = subkey.split('/')

    d = _expand_dict(self._dict, keylist)

    last_key = keylist[-1]
    d[last_key] = _dict_merge(d.get(last_key, {}), value)
    if self.save_path:
      dirname = os.path.dirname(self.save_path)
      if not os.path.exists(dirname):
        os.makedirs(dirname)
      with open(self.save_path, 'w') as f:
        pickle.dump(self._dict, f)

  def export(self):
    """Export the properties to a map suitable for JSONificaiton"""
    return copy.deepcopy(self._dict)

  def update_in(self, *args):
    """Assign a value by treating the arguments as elements in a key path, 
    except the final argument which is used as the value

    >>> p = Properties()
    >>> p.update_in('one', 'two', 'three', 4)
    >>> p.export()
    {'one': {'two': {'three': 4}}}"""
    self["/".join(args[:-1])] = args[-1]

  def get_in(self, *args):
    """Get a value by treating the arguments as elements in a key path

    >>> p = Properties()
    >>> p['one/two/three'] = 4
    >>> p.get_in('one', 'two', 'three')
    4"""
    return self["/".join(args)]
