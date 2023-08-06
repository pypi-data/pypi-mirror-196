from Crypto.Hash import SHA256

class NamedObjSet():
    ''' A set of case-insensitive named objects
    '''
    def __init__(self, cache={}, prefix=''):
        self.cache, self.prefix = cache, prefix
        self.objs = cache.get(f"{prefix}", {})
        self._hash = cache.get(f"{prefix}.hash", None)


    def clear(self):
        self.objs.clear()
        self._hash = None


    def save(self):
        self.cache[f"{self.prefix}"] = self.objs
        self.cache[f"{self.prefix}.hash"] = self._hash


    def hash(self):
        if self._hash == None:
            h = SHA256.new()
            for obj in self: h.update(f'{obj:fingerprint}'.encode('utf8'))
            self._hash = h.digest()
        return self._hash


    def add(self, obj):
        name = obj.name.lower()
        if name in self.objs:
            self.objs[name].merge(obj)
        else:
            self.objs[name] = obj
        self._hash = None
        return obj


    def add_from(self, other):
        for o in other:
            self.add(o.__class__.clone(o))


    def keys(self):
        return self.objs.keys()


    def __getitem__(self, item):
        return self.objs[(item if isinstance(item, str) else item.name).lower()]


    def __contains__(self, item):
        return (item if isinstance(item, str) else item.name).lower() in self.objs


    def __iter__(self):
        for k in sorted(self.objs.keys()):
            yield self.objs[k]
        