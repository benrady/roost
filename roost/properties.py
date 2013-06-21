import copy

def _dict_merge(a, b):
  '''recursively merges dict's. not just simple a['key'] = b['key'], if
  both a and bhave a key who's value is a dict then dict_merge is called
  on both values and the result stored in the returned dictionary.'''
  if not isinstance(b, dict):
    return b
  if not isinstance(a, dict):
    a = {a: None}
  result = copy.deepcopy(a)
  for k, v in b.iteritems():
    if k in result and isinstance(result[k], dict):
      result[k] = dict_merge(result[k], v)
    else:
      result[k] = copy.deepcopy(v)
  return result 

def _build_map(keylist, val):
  if len(keylist) == 0:
    return val
  return {keylist[0]: _build_map(keylist[1:], val)}

class Properties(dict):

  def __getitem__(self, subkey):
    if self.has_key(subkey):
      return dict.__getitem__(self, subkey)
    return None
    #children = [key.split('/') for key, val in self.items() if key.startswith(subkey)]
    #return children

  def __setitem__(self, subkey, value):
    '''Set a value, merging keys and values in a dict onto a subkey in the properties'''
    if isinstance(value, dict):
      for key, val in value.items():
        dict.__setitem__(self, subkey + '/' + key, val)
    else:
      dict.__setitem__(self, subkey, value)

  def export(self):
    '''Converts the property heirarchy to a dict (of dicts...depending on the data)'''
    result = {}
    for key, val in self.items():
      keylist = key.split('/')
      result[keylist[0]] = _dict_merge(result.get(keylist[0], {}), _build_map(keylist[1:], val))
    return result

  def update_in(self, *args):
    self["/".join(args[:-1])] = args[-1]

  def get_in(self, *args):
    return self["/".join(args)]
