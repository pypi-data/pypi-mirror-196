
import logging
from subprocess import Popen, PIPE, DEVNULL

log = logging.getLogger('grep')

def grep_group_cmds(groups, pattern, *args):
    base = ['grep'] + list(args)
    for mod, locs in groups.items():
        for loc in locs:
            if loc[0]:
                exclude = [f'--exclude={e}' for e in loc[2:]]
                include = [f'--include=*.{e.strip()}' for e in loc[0].split(',') if e.strip()]
                cmd = base + include + exclude + ['-r', pattern, loc[1]]
            else:
                cmd = base + [pattern] + list(loc[1:]) + ['/dev/null']
            log.debug(' '.join(cmd))
            yield mod, cmd




def grep_groups(groups, pattern, *args):
    g = {}
    for m, p in [(m, Popen(cmd, stderr=DEVNULL, stdout=PIPE)) for m, cmd in grep_group_cmds(groups, pattern, *args)]:
        g.setdefault(m,'')
        g[m] += p.communicate()[0].decode('utf8')
    return g




def grep_files(files, pattern, *args):
    if not files: return ''
    cmd = ['grep', '--color=never'] + list(args) + [pattern] + files
    log.debug(f"Grep files: {' '.join(cmd)}")
    return Popen(cmd, stderr=DEVNULL, stdout=PIPE).communicate()[0].decode('utf8')




class SLOC():
    def __init__(self, fname):
        self.fname = fname
        self.dir, fname = os.path.split(fname)
        self.name, self.ext = os.path.splitext(fname)
        self.bytes = {k:0 for k in 'src lines cmt doc str gen'.split(' ')}
        fn = f"parse{self.ext.replace('.','_')}"
        if hasattr(self, fn): getattr(self, fn)()

    def parse_py(self):
        with open(self.fname, 'r') as f:
            code = f.read()
        

                

