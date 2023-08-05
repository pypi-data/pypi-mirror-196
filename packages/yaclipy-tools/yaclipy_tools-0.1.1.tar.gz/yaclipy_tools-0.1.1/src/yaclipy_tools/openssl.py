

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

