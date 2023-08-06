import os, logging, re
from cli import print, exit, CLR
from ..secrets import OpenSSL

log = logging.getLogger('file')


class Scraper():
    def __init__(self, name, kw, regex):
        for k,v in {'_re':None, 'name':name, 'kw':kw, 'regex':regex}.items():
            setattr(self, k, v)
        
    def re(self):
        if not self._re:
            self._re = re.compile(self.regex)
        return self._re
    
    def __repr__(self):
        return f"{self.name}|{self.kw}"

    def __hash__(self):
        return hash(str(self))




class File():
    ''' Scrape objects and their leading documentation
    '''
    re_gen = None
    
    def __init__(self, fname):
        self.fname = fname
        self.scrapers = {}
        self.cmt = {'.py':'###'}.get(os.path.splitext(fname)[1], '///')
        self.modified = False
        self._lines = None
        self._hash = None


    def __lt__(self, other):
        return self.fname < other.fname
        

    def add_scraper(self, scraper, callback):
        self.scrapers[scraper] = callback
        return self


    def hash(self):
        if self._hash == None:
            self._hash = OpenSSL().file_hash(self.fname)
        return self._hash


    def scrape(self):
        scrapers = [(s.re(), s.kw, c) for s,c in self.scrapers.items()]
        log.debug(f"scrape: {', '.join(map(str, self.scrapers))} -- {self.fname}")
        doc = []
        added = 0
        for lno, line in enumerate(self.lines()):
            ls = line.lstrip()
            if ls.startswith(self.cmt):
                doc.append(ls[4:].rstrip())
                continue
            for regex, kw, callback in scrapers:
                if kw and kw not in line: continue
                if m := regex.match(line):
                    added += 1
                    callback(doc=doc[:], fname=self.fname, lno=lno+1, **m.groupdict())
                elif kw:
                    exit(print.ERR, f"Coudn't parse {kw} definition.~lang ja~「{kw}」の定義を解析できなかった。", 
                        ['']*3, line, ['']*2, CLR.lb, regex.pattern, CLR.x, ['']*2, f'{CLR.a}{self.fname}:{lno+1}{CLR.x}')
            doc = []
        log.debug(f"scraped: {added} objects -- {self.fname}")
        return self
        

    def replace(self, code, permanent=False):
        ''' Replace lines starting and ending with ~gen~ tags, or single lines with ~gen~ at the end.
        '''
        if not File.re_gen: File.re_gen = re.compile(r'^(\s*)(.*?)(([.]+|/+|#+)\s+)?~gen~\s+(\w+)(.*)$')
        log.debug(f"replace  {' '.join(list(code.keys()))} -- {self.fname}")
        code = {k:((lambda *args, v=v: v) if isinstance(v, list) else v) for k,v in code.items()}
        lines = self.lines()
        iend = 0
        i = len(lines) - 1
        while i >= 0:
            if (m:=File.re_gen.match(lines[i])) and m[5] in code:
                indent, single_line, cmt, _, name, postfix = m.groups()
                if single_line:
                    lines[i:i+1] = [f'{indent}{l}'+('' if j or permanent else f' {cmt}~gen~ {name}{postfix}') + '\n'
                        for j,l in enumerate(code[name]([single_line], name, postfix))]
                elif iend:
                    lines[i + int(not permanent):iend] = [indent + l + '\n' for l in code[name](lines[i + 1:iend - int(permanent)], name,  postfix)]
                    iend = 0
                else:
                    iend = i + int(permanent)
            i -= 1
        self.modified=True
        return self


    def lines(self):
        if self._lines == None:
            with open(self.fname) as f:
                self._lines = f.readlines()
        return self._lines


    def __getitem__(self, lno):
        return self.lines()[lno-1]
    

    def __setitem__(self, lno, text):
        cur = self[lno]
        self.lines()[lno-1] = text
        if cur != text: self.modified = True


    def save(self):
        if self.modified:
            log.info(f"write -- {self.fname}")
            with open(self.fname, 'w') as f:
                for l in self._lines:
                    f.write(l)
            self._hash = None
        self._lines = None
        self.modified = False
        

    def __repr__(self):
        return f"{self}"


    def __format__(self, spec):
        return f"<{self.fname} " + ' '.join(map(str, self.scrapers)) + '>'
