import os, sys
from cli import CLI, print, Text, CLR, exit, Table, run
from .vault import Vault, GPG, File


@CLI()
def ls():
    ''' Show status information about the files in the vault.
    ~lang ja~
    vault内のファイルに関する情報を表示します。

    Unlocked files (yellow) are on the disk in a clear-text format.
    For enhanced security they should only be unlocked when needed.::
    ~lang ja~
    ロック解除されたファイル（黄色）は、クリアテキスト形式でディスク上にあります。
    セキュリティを強化するには、必要な場合にのみロックを解除する。::
    
       $ ./cli.py vault lock

    Untracked files (gray) must be added before they can be pushed::
    ~lang ja~追跡されていないファイル（灰色）は、プッシュする前に追加する必要があります。::

       $ ./cli.py vault lock -a <filename>
    '''    
    print.ln([f"{f:fancy}" for f in Vault().files()])




@CLI()
def members(*, join=False):
    ''' Show the members that can unlock the vault.
    ~lang ja~vaultのロックを解除できるメンバーを表示します。

    Parameters:
        --join
            Add your GPG public key to the vault.
            ~lang ja~GPG公開鍵をvaultに追加します。
    '''
    member = False
    tbl = Table(0,0, sides=0, just0='^>')
    for name, email, me, _ in Vault().members():
        member |= me
        tbl((CLR.bld if me else CLR.x, name, CLR.x))
        tbl((' ', CLR.a, f'<{email}>', CLR.x))
    print('',tbl,'')
    if not join: 
        if not member: exit(print.WARN, "You are not a member. Run with ``./cli.py vault members --join`` to join. ~lang ja~あなたはメンバーではない。「--join」で実行すれば参加できる。", )
        return

    def _choose():
        users = list(GPG().list_users())
        if not users: return None
        print.ln("Which user do you want to add to the vault?~lang ja~vaultに参加するユーザーを選択してください：")
        tbl = Table(0,1,0,0, color0=CLR.y, color2=CLR.a, just1='^>', sides=0)
        for i, u in enumerate(users):
            tbl(i+1,')', ' ' + u.name, f' <{u.email}>')
        tbl(i+2, ')', ' Create a new user', '')
        print(tbl)
        while True:
            try:
                uid = int(input(f"? "))
                assert(uid > 0 and uid <= len(users)+1)
                break
            except KeyboardInterrupt:
                print("")
                sys.exit(1)
            except:
                continue
        return None if uid == len(users)+1 else users[uid-1]

    usr = _choose()
    if not usr:
        GPG().genkey()
        usr = _choose()
    mdir = os.path.relpath(Vault().path('members'))
    print.ln(f'''
        Adding public key to `{mdir}`.
        Make sure to `./cli.py vault push` the vault so another member can re-lock the files for you.
        ~lang ja~「{mdir}」に公開鍵を追加します。
         別のメンバーがファイルを再ロックできるように「./cli.py vault push」してください。''')
    GPG().export_key(usr.email, Vault().path('members', usr.email))



def _conflicts(conflict):
    if conflict:
        print.ln(print.ERR, "Conflicts that need to be resolved:~lang ja~解決する必要のある競合：", ['']*3, [f'  - {f}' for f in conflict])


@CLI()
def unlock(*paths, verbose__v=False, quiet=False):
    ''' Unlock one or all the encrypted ``.gpg`` files in the vault.
    ~lang ja~
    vault内の暗号化された「.gpg」ファイルの1つまたはすべてのロックを解除します。

    Parameters:
        [path]
            Files or directories to unlock.  The default is the root vault directory.
            ~lang ja~暗号化を解除するファイルまたはディレクトリ。 デフォルトはルートボールトディレクトリです。
        --verbose, -v
            Show verbose gpg output
        --quiet
            Don't show any output

    Examples:
        Unlock a single file (.gpg is optional)::
           $ ./cli.py vault unlock services/vault/*.txt

        Unlock all files in a directory::
           $ ./cli.py vault unlock services/vault/sub/path/

    '''
    conflict = []
    failed = []
    unlocked = []
    for f in Vault().files(list(paths)):
        if str(f).endswith('.gpg') or not f&File.GPG: continue
        code = Vault().decrypt(f'{f}.gpg', verbose__v)
        {'d':unlocked, 'e':failed, 'c':conflict}[code].append(f)

    if quiet: return
    if unlocked:
        print.ln([f'  {f}' for f in unlocked])
    else:
        print.ln("Nothing unlocked~lang ja~ロックが解除されたものがない")
    if failed:
        print.ln(print.WARN, '''Some files failed to decrypt. These files must be encrypted for you by one of the other members.
        ~lang ja~一部のファイルは復号化に失敗しました。これらのファイルは、他のメンバーが暗号化する必要があります。
        ''', ['']*3, [f'  - {f}' for f in failed])
    _conflicts(conflict)




@CLI()
def lock(*paths, add__a=False, verbose__v=False):
    ''' Lock files and directories.
    ~lang ja~ファイルまたはディレクトリをロックする。

    The .gitignore file by default ignores all files in the vault execpt ``.gpg``
    files.  To add a clear-text file to the vault you must add an appropriate git exception rule to .gitignore.
    ~lang ja~
    .gitignoreファイルは、デフォルトで、.gpgファイル以外すべてのファイルを無視します。
    クリアテキストファイルをvaultに追加するには、適切なgit例外ルールを.gitignoreに追加する必要があります

    Parameters:
        [paths]
            A list of files and directories to lock.  The default is to lock all files in the vault.
            ~lang ja~ロックするファイルまたはディレクトリのリスト。 デフォルトでは、vault内のすべてのファイルがロックされます。
        --verbose, -v
            verbose GPG output
        --add, -a
            Add new files.  By default only files that have been added previouly are locked.
            ~lang ja~新しいファイルを追加します。 デフォルトでは、以前に追加されたファイルのみがロックされます。
    '''
    locked = []
    conflict = []
    for f in Vault().files(paths):
        if f&File.CONFLICT:
            conflict.append(f)
        elif (f&File.GPG and not f&File.NOEXIST) or (add__a and not f&File.TRACKED):
            Vault().encrypt(f)
            locked.append(f)
    if locked:
        print.ln([f'🔒{f}' for f in locked])
    elif not conflict:
        print.ln('Nothing to lock~lang ja~ロックする必要がない')
    _conflicts(conflict)




@CLI()
def push():
    ''' Lock the vault and ``git push`` it to remote origin.
    ~lang ja~
    vaultをロックしてから``git push``する。

    .. warning:

       Don't manually git push the vault contents.
       ~lang ja~
       vaultの内容を手動でgitpushしないでください。

    We don't want to track the file history so we always ``--amend`` and
    force pushing.
    ~lang ja~
    ファイル履歴を追跡したくないので、常に `` --amend``と強制的に押している。
    '''
    lock()
    for f in Vault().files():
        if f&File.CONFLICT:
            exit("Must resolve conflicts before pushing")
    Vault().commit()
    Vault().repo.push(force=True)



@CLI()
def status():
    ''' Show the git status of the repository
    '''
    status = Vault().repo.status()
    print.ln([f'{s} {f}' for s,f in status] if status else 'Up to date')
    print.ln(CLR.o,"Members~lang ja~メンバー",CLR.x, ':')
    members()



@CLI()
def pull():
    ''' Pull from the remote origin.~lang ja~remote originからプルします。

    If you have local changes to clear-text files that you want to merge manually then
    you can manually run git pull::
    ~lang ja~
    手動でマージするクリアテキストファイルにローカルな変更がある場合は、
    手動でgitpullを実行できます::

       $ git -C services/vault pull --rebase
    '''
    unlock(quiet=True)
    Vault().commit()
    Vault().repo.pull_rebase('-X','theirs')
    unlock()
    



@CLI()
def rm(file):
    ''' Write random bytes over the top of a file before deleting it.
    ~lang ja~ファイルを削除する前に、ファイルの上にランダムなバイトを書き込みます。

    This is overkill and probably doesn't help on SSD filesystems.
    ~lang ja~これはやり過ぎであり、SSDファイルシステムではおそらく役に立ちません。

    Parameters:
        <path>, --file <path>
            A file to remove
    '''
    File.rm(file)

