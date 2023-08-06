import os, logging, sys, re, time, random
from cli import COMMON_DIR, run, print, exit, CLR, Text, confirm
from .git import Git
from .make import File
from service_abc.make import File as MakeFile

log = logging.getLogger('vault')





class Vault():

    _instance = None

    def __new__(cls):
        if Vault._instance: return Vault._instance 
        return super().__new__(cls)
        

    def __init__(self, origin='git@github.com:IMMERSIVE-SESSIONS/framelunch_vault.git', repo=f'{COMMON_DIR}/vault'):
        if Vault._instance: return
        Vault._instance = self
        self.repo = Git(repo)
        self._members = None
        try:
            self.repo.name()
        except:
            run(['git', 'clone', origin, repo])


    def path(self, *parts):
        return os.path.join(str(self.repo), *parts)


    def members(self, force=False):
        if not self._members or force:
            self._members = [GPG().import_key(self.path('members', usr)) for usr in os.listdir(self.path('members'))]
        return self._members

    
    def files(self, paths=None):
        if not paths: paths = [str(self.repo)]
        paths = [os.path.relpath(p, str(self.repo)) + ('/' if os.path.isdir(p) else '') for p in paths]
        paths = set(p[:-4] if p.endswith('.gpg') else p for p in paths)
        # Initalize tracked, untracked, non-existant
        files = FileSet()
        for f in self.repo.list(invert=True): files.add(f)
        for f in self.repo.list(): files.add(f, File.TRACKED)
        for t,f in self.repo.status(changes_only=True):
            if 'D' in t: files.get(f).flags |= File.REM
        # Collect files matching paths
        used = set()
        fout = []
        for f in sorted(files):
            if p:=f.matches(paths):
                used.add(p)
                fout.append(f)
        if len(used) != len(paths):
            exit(print.ERR, "Files not found:", ['']*3, [f" - {os.path.relpath(f'{self.repo}/{p}')}" for p in set(paths)-used])
        return fout


    def encrypt(self, fname, verbose=False):
        fname = self.path(str(fname))
        users = [c for members in (['-r', u.key] for u in self.members()) for c in members]
        run(['gpg', '-e', '--yes', '--trust-model', 'always'] + users + [fname], silent=not verbose)
        File.rm(fname)


    def decrypt(self, fname, verbose=False):
        fname = self.path(str(fname))
        orig = out = os.path.splitext(fname)[0]
        if os.path.exists(out): out = out + '.orig'
        try:
            run(['gpg', '--decrypt', '--yes', '--batch', '--output', out, fname], silent=not verbose)
        except:
            return 'e'
        if orig != out: 
            try:
                run(['diff', orig, out], silent=True)
                File.rm(out)
            except:
                return 'c'
        return 'd'
                

    def commit(self):
        dirkeep = set()
        delete = []
        for f in self.files():
            if f&File.REM: delete.append(f)
            fname = os.path.split(str(f))[0]
            dirkeep.add(fname)
            while os.path.basename(fname) != fname:
                dirkeep.add(fname)
                fname = os.path.basename(fname)
        dirkeep.discard('')
        if delete:
            confirm([f'{f:fancy}' for f in delete], ['']*3, '''Are you sure you want to delete these files?
            Deleted files will be lost forever if pushed.
            ~lang ja~これらのファイルを削除してもよろしいですか？
            削除されたファイルは、プッシュされると永久に失われます。''',['']*2,'y/N: ')
        MakeFile(self.path('.gitignore')).replace({'FOLDERS':sorted([f'!/{d}/' for d in dirkeep])}).save()
        self.repo.amend_all('vault')
