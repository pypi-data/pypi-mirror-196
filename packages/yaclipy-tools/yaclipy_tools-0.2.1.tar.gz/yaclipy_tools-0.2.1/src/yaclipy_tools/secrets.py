import logging, os, sys, re
from cli import print, run, exit, CLR

log = logging.getLogger('secrets')



class OpenSSL():

    _instance = None

    def __new__(cls):
        if OpenSSL._instance: return OpenSSL._instance
        return super().__new__(cls)


    def __init__(self):
        if OpenSSL._instance: return
        OpenSSL._instance = self
        self.openssl = os.path.join(os.environ.get('OPENSSL3', '/usr/local/opt/openssl/bin'), 'openssl')
        if not os.path.exists(self.openssl):
            self.openssl = 'openssl'
        try:
            ver = run([self.openssl, 'version', '-v'], read=True, or_else='Unknown ', msg='').split(' ')
            assert(ver[0] == 'OpenSSL')
            assert(ver[1][0] == '3')
        except:
            print.ln(print.ERR, "Incompatable openssl found: ~lang ja~互換性のないopenssl: ", ' '.join(ver))
            print.ln("Get OpenSSL 3.x and / or set OPENSSL3 and try again.~lang ja~OpenSSL 3.xを入手して、再試行してください。 PATHにopensslがなければ「OPENSSL3」の環境変数の設定が必要",)
            exit("   $ brew install openssl")


    def cert_show(self, prefix, mode='-subject'):
        run([self.openssl, 'x509', '-in', prefix+'.pem', mode, '-noout'])


    def cert(self, *, prefix, cn, ca, san=[], client=False, force=False, askpass=False, days=365):
        log.info(f"Openssl '{prefix}'  {ca}  {cn}  {san}")

        if not force and os.path.exists(prefix+'.pem'):
            self.cert_show(prefix, '-text')
            exit(print.ERR, "Certificate exists.  Use `--force` to overwrite")
        os.makedirs(os.path.split(prefix)[0], exist_ok=True)
        subj=f'/O=cli.py/CN={cn}'
        #subjcn = ''.join([f'/CN={cn}' for cn in cn if '*' not in cn])
        sancn = ','.join([f'IP:{x}' if re.search(r'^[0-9.:]+$',x) else f'DNS:{x}' for x in san])

        cmd = [self.openssl, 'req', '-x509', '-sha256', '-out', prefix+'.pem', '-newkey', 'rsa:2048', '-keyout', prefix+'-key.pem', '-days', str(days), '-subj', subj]
        if not askpass:
            cmd += ['-noenc']
        if ca:
            cmd += ['-CA', ca+'.pem']
            cmd += ['-CAkey', ca+'-key.pem']
            cmd += ['-addext', 'basicConstraints=critical,CA:FALSE']
            cmd += ['-addext', 'subjectKeyIdentifier=none']
            if client:
                cmd += ['-addext', 'extendedKeyUsage=clientAuth']
            else:
                #Key Usage: critical, Digital Signature, Key Encipherment
                cmd += ['-addext', 'extendedKeyUsage=serverAuth']
        else:
            cmd += ['-addext', 'basicConstraints=critical,CA:TRUE']
            cmd += ['-addext', 'keyUsage=critical,keyCertSign']
            cmd += ['-addext', 'subjectKeyIdentifier=hash']
            cmd += ['-addext', 'authorityKeyIdentifier=none']
        if sancn:
            cmd += ['-addext', f'subjectAltName={sancn}']
        
        
        run(cmd)
        self.cert_show(prefix)


    def rsa(self, *, path, format):
        run([self.openssl, 'genrsa', '-traditional', '-out', path])


    def hex(self, *, path, nbytes=32):
        run([self.openssl, 'rand', '-hex', '-out', path, str(nbytes)])


    def file_hash(self, fname):
        return bytes.fromhex(run([self.openssl, 'dgst', '-sha256', '-hex', '-r', fname], read=True, msg='', or_else='').split(' ',1)[0])




class Secret():
    def __init__(self, *, cfg, name='x'):
        self.cfg = cfg
        self.name = name


    def ensure(self):
        try:
            self.load()
        except:
            self.gen()
            self.load()


    def load(self, mode, path=None):
        with open(path or str(self), mode) as f:
            return f.read()


    def __str__(self):
        return f"{self.cfg.secrets_dir}/{self.name}"




class SecretCert(Secret):
    def __init__(self, *, cn=None, ca=None, san=[], **kwargs):
        self.cn = cn
        self.ca = ca
        self.san = san
        super().__init__(**kwargs)


    def paths(self):
        return (f'{self}-key.pem', f'{self}.pem')


    def gen(self):
        print.ln("GEN", repr(self))
        assert(self.cn), f"No common names defined for '{self.name}'"
        OpenSSL().cert(prefix=str(self), cn=self.cn, ca=f'{self.cfg.secrets_dir}/{self.ca}' if self.ca else None, san=self.san, client='client' in self.cn.lower(), force=True)


    def load(self):
        return tuple(super(SecretCert, self).load('rb', p) for p in self.paths())

    def __repr__(self):
        return f'<cert> {self.name}  [{self.cn}; {self.san}; {self.ca}]'


class SecretAES(Secret):
    def __init__(self, nbytes=16, **kwargs):
        self.nbytes = nbytes
        super().__init__(**kwargs)


    def load(self):
        raw = super().load('r')
        assert(len(raw) == self.nbytes*4 + 1), f'bad length {len(raw)} != {self.nbytes*4 + 1}'
        return (bytes.fromhex(raw[:self.nbytes*2]), bytes.fromhex(raw[self.nbytes*2:-1]))


    def gen(self):
        OpenSSL().hex(path=f'{self.cfg.secrets_dir}/{self.name}', nbytes=self.nbytes*2)




class SecretRSA(Secret):
    def __init__(self, format='pkcs#1', **kwargs):
        self.format = format
        super().__init__(**kwargs)


    def load(self, **kwargs):
        return super().load('rb')


    def gen(self):
        OpenSSL().rsa(path=f'{self.cfg.secrets_dir}/{self.name}', format=self.format)




class SecretValue(Secret):
    def __init__(self, *, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)


    def gen(self):
        os.makedirs(self.cfg.secrets_dir, exist_ok=True)
        with open(f'{self.cfg.secrets_dir}/{self.name}', 'wb' if isinstance(self.value, bytes) else 'w') as f:
            f.write(self.value)


    def load(self):
        return super().load('rb' if isinstance(self.value, bytes) else 'r')


    def __repr__(self):
        return f'<SecretValue> {self.name}'


