import logging, os, inspect
from .file import File, Scraper
from .op import MakeOp
from .no_set import NamedObjSet
from .cache import MakeCache

log = logging.getLogger('root-op')

class RootOp(MakeOp):
    def __init__(self, **kwargs):
        super().__init__(cache=MakeCache(), prefix='', files={}, ops={}, **kwargs)


    def file(self, fname):
        fname = os.path.relpath(fname)
        if fname not in self.files:
            self.files[fname] = File(fname)
            log.debug(f"New File : {fname}")
        return self.files[fname]


    def spawn(self, kls, **kwargs):
        kwargs.setdefault('prefix', f"{kls.__name__}")
        kwargs.setdefault('cache', self.cache)
        spec = inspect.getfullargspec(kls.__init__)
        for need in set(spec.kwonlyargs) - set(kwargs.keys()):
            kwargs[need] = getattr(self, need)
        self.ops[kwargs['prefix']] = kls(root=self, **kwargs)
        return self.ops[kwargs['prefix']]

    
    def done(self):
        for f in self.files.values(): f.save()
        log.debug(f"Done : {len(self.files)} files,  {len(self.ops)} ops")
        self.files = {}
        for k,v in self.ops.items():
            self.cache[f"{k}.hash"] = v.hash(force=True)
        self.cache.save()

    
    def ensure(self, kls, **kwargs):
        self.spawn(kls, **kwargs).ensure()
        self.done()
        

    def __getitem__(self, prefix):
        return self.ops[prefix]
