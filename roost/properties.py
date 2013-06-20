import copy

def dict_merge(a, b):
  '''recursively merges dict's. not just simple a['key'] = b['key'], if
  both a and bhave a key who's value is a dict then dict_merge is called
  on both values and the result stored in the returned dictionary.'''
  if not isinstance(b, dict):
    return b
  result = copy.deepcopy(a)
  for k, v in b.iteritems():
    if k in result and isinstance(result[k], dict):
      result[k] = dict_merge(result[k], v)
    else:
      result[k] = copy.deepcopy(v)
  return result 

class Properties(dict):

  def export(self, extras):
    return dict_merge(self, extras)

  def save(self, path, value):
    d = self
    keys = path.split('/')
    for k in keys[:-1]: 
      if not d.has_key(k):
        d[k] = {}
      d = d[k]

    d[keys[-1]] = value


