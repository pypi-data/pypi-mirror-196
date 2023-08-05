import os, sys
from cli import CLI, run, print, CLR, exit, Text

class Git():
    def __init__(self, repo):
        self.repo = os.path.abspath(repo)


    def name(self):
        if not hasattr(self, '_name'):
            l = run(['git','-C',self.repo,'config','--get','remote.origin.url'], read=True, msg=False, or_else='').strip()
            if not l: l = run(['git','-C',self.repo,'rev-parse','--show-toplevel'], read=True, msg=False).strip()
            self._name = os.path.splitext(os.path.basename(l))[0]
        return self._name


    def current_commit(self):
        return run(['git','-C',self.repo,'rev-parse','HEAD'], msg=False, read=True).strip()


    def status(self, changes_only=False):
        changes = [x for x in run(['git','-C',self.repo,'status','-z'], read=True, msg=False).split('\0') if x]
        changes = [(k[:2],k[3:]) for k in changes]
        if changes or changes_only: return changes
        if run(['git', '-C', self.repo, 'fetch', '--dry-run'], read=True, msg=False).strip():
            return [('  ','Need to pull')]
        if run(['git', '-C', self.repo, 'status', '-sb'], read=True, msg=False).splitlines()[0].split('[')[-1].startswith('ahead'):
            return [('  ','Need to push')] 
        return []


    def current_branch(self):
        return run(['git', '-C', self.repo, 'symbolic-ref', '--short', 'HEAD'], msg=False, read=True).strip()


    def up_to_date(self):
        return not bool(self.status())


    def list(self, *pattern, invert=False):
        return run(['git', '-C', self.repo, 'ls-files'] + list(pattern) + (['--other'] if invert else []), msg=False,read=True).splitlines()


    def amend_all(self, msg):
        run(['git','-C',self.repo,'add','.'])
        run(['git','-C',self.repo,'commit', '--amend', '-m', msg])


    def pull_rebase(self, *args):
        run(['git','-C',self.repo,'pull','--rebase'] + list(args))


    def push(self, *args, force=False):
        run(['git', '-C', self.repo,'push'] + (['--force-with-lease'] if force else []) + list(args) )


    def __str__(self):
        return self.repo




@CLI()
def status(repo):
    ''' git status

    Parameters:
        <repo>, --repo
            ~parent~
    '''
    g = Git(repo)
    status = g.status()
    print(Text(CLR.m, g.current_branch(), CLR.x))
    if status:
        print(*[f'{s} {f}' for s,f in status])
    else: print(Text(CLR.lg, 'Up to date', CLR.x))




@CLI()
def commit(repo, *, message__m):
    ''' Commit all (`-a` flag is implied)

    Parameters:
        <repo>, --repo
            ~parent~
        --message <str>, -m <str> | required
            Commit message
    '''
    run(['git', '-C', repo, 'commit', '-am', message__m], msg=False, success=[0,1])




@CLI()
def push(repo):
    ''' git push

    Parameters:
        <repo>, --repo
            ~parent~
    '''
    run(['git', '-C', repo, 'push'], msg=False, success=[0,1])




@CLI()
def pull_rebase(repo):
    ''' git pull --rebase

    Parameters:
        <repo>, --repo
            ~parent~
    '''
    if os.path.isfile(f'{repo}/cli.py') and os.path.isfile(f'{repo}/config.py'):
        run([f'{repo}/cli.py', 'configure', '-s'])
    run(['git', '-C', repo, 'pull', '--rebase'], msg=False, success=[0,1])




@CLI()
def rebase_ff(repo, base, ontop):
    ''' Rebase and then ff merge

    Parameters:
        <repo>, --repo
            ~parent~
        <branch>, --base <branch> | required
            The branch to apply changes to.
        <branch>, --ontop <branch> | required
            The branch containing new commits.
    '''
    run(['git', '-C', repo, 'rebase', base, ontop])
    run(['git', '-C', repo, 'switch', base])
    run(['git', '-C', repo, 'merge', '--ff-only', ontop])




@CLI()
def hooks_install(repo):
    ''' install pre-commit hook that runs './cli.py configure' so that you don't forget.
    
    Parameters:
        <repo>, --repo
            ~parent~
    '''
    lines = '''        #!/bin/sh
        if ! git symbolic-ref -q HEAD >/dev/null 2>&1; then
            exit 0
        fi
        git status -z > local/pre-commit
        ./cli.py configure -s >/dev/null 2>&1
        git status -z > local/pre-commit2
        if ! diff local/pre-commit local/pre-commit2 >/dev/null 2>&1; then
            cat <<\EOF

        \x1b[1;31mStopping commit\x1b[0m

        After running './cli.py config' the source code changed.
        Check the new git status above and try the commit again.

        EOF
            exit 1
        fi
    '''
    if not (os.path.isfile(f'{repo}/cli.py') and os.path.isfile(f"{repo}/config.py")):
        exit(print.ERR, f"Not installing hooks")
    print.ln(f"Installing pre-commit hook")
    with open(f'{repo}/.git/hooks/pre-commit', 'w') as f:
        for l in lines.split('\n'):
            f.write(l[8:]+'\n')
    os.chmod(f'{repo}/.git/hooks/pre-commit', 0o755)
