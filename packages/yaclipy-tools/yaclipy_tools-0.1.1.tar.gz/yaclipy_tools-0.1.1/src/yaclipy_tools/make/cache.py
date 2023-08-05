import os, logging, pickle

log = logging.getLogger('make-cache')

class MakeCache(dict):

    fname = 'local/make_cache.pickle'
    modified = False
    _instance = None

    @classmethod
    def clean(self):
        try: os.remove(MakeCache.fname)
        except: pass


    def __init__(self, fname=fname):
        try:
            with open(MakeCache.fname, 'rb') as f:
                super().__init__(pickle.load(f))
        except Exception as e:
            log.info(f"Cach loading error: {e}")
        MakeCache.modified = False


    def __setitem__(self, k, v):
        MakeCache.modified |= k not in self or v!=self[k]
        super().__setitem__(k,v)


    def save(self):
        if not MakeCache.modified: return
        log.debug(f"Save: {self.keys()}")
        with open(MakeCache.fname, 'wb') as f:
            pickle.dump(self, f)
        MakeCache.modified = False
