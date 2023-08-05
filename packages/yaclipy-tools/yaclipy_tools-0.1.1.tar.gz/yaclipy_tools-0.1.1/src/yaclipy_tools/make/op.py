import logging, inspect
from Crypto.Hash import SHA256

log = logging.getLogger('make-op')

class MakeOp():
    def __init__(self, *, prefix, cache, **kwargs):
        kwargs.update({'prefix':prefix, 'cache':cache})
        for k,v in kwargs.items():
            setattr(self, k, v)
        self._hash = None


    def deps(self): return []

    def execute(self): pass
    
    
    def spawn(self, kls, **kwargs):
        spec = inspect.getfullargspec(kls.__init__)
        for need in set(spec.kwonlyargs) - set(kwargs.keys()):
            if hasattr(self, need): kwargs[need] = getattr(self, need)
        kwargs.setdefault('prefix', f"{self.prefix}.{kls.__name__}")
        return self.root.spawn(kls, **kwargs)
        

    def ensure(self):
        hash = self.cache.get(f'{self.prefix}.hash', None)
        if hash and hash == self.hash(): return True
        log.info(f'EXE: {self.prefix}')
        self.execute()


    def hash(self, force=False):
        if not force and self._hash: return self._hash
        h = SHA256.new()
        for data in self.deps():
            h.update(data if isinstance(data, bytes) else str(data).encode('utf8'))
            h.update(b'0')
        self._hash = h.digest()
        return self._hash
