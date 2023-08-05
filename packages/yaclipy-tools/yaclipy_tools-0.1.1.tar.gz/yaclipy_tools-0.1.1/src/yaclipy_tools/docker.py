
class Docker():
    @staticmethod
    def get_config(force=False):
        if not run('docker image ls', msg='', or_else='', read=True):
            exit(print.ERR, f"Start docker desktop and try again.~lang ja~Dockerを起動して、再試行してください。")
        cfg = Config()
        if not force and not cfg.docker:
            exit(print.ERR, f'''The target '{cfg.target}' doesn't define a docker image.
                ~lang ja~'{cfg.target}'のtargetにはDockerイメージを定義してない。''')
        return cfg


    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


    def build(self, target=None, nocache=False, **kwargs):
        print.hr()
        print.ln(self.lines)
        print.hr()
        env = os.environ.copy()
        env['DOCKER_BUILDKIT'] = '1'
        cmd = ['docker', 'build', '-t', self.name]#, '--progress', 'plain']
        for k,v in kwargs.items():
            cmd += ['--label', f'{k}={v}']
        if target: cmd += ['--target', target]
        #if nocache: cmd += ['--no-cache']
        cmd += ['-f-', self.context]
        if subprocess.run(cmd, input='\n'.join(self.lines).encode('utf8'), env=env).returncode:
            exit(print.ERR, "Docker Build failed~lang ja~Dockerビルドが失敗しました", ['']*3, ' '.join(cmd))


    def run(self, interactive=True, remove=True, command=None, raw_cmd=False):
        cmd = ['docker', 'run']
        # Network
        if hasattr(self, 'network'):
            try:
                run(f'docker network inspect {self.network}', read=True, msg='', err='')
            except:
                run(f'docker network create {self.network}', read=True, msg='')
            cmd += [f'--network={self.network}']
        # name
        cmd += ['--name', self.name if '/' not in self.name else self.name.rsplit('/',1)[1].split(':')[0]]
        #
        if interactive: cmd += ['-it']
        if remove: cmd += ['--rm']
        # Environment
        if hasattr(self, 'env'):
            for k,v in self.env.items():
                cmd += ['-e',f'{k}={v}']
        # Volumes / binds
        if hasattr(self, 'binds'):
            for host, container in self.binds:
                cmd += ['--mount', f'type=bind,source={host},target={container}']
        #cmd += ['-v', '/var/run/docker.sock:/var/run/docker.sock']
        if hasattr(self, 'endpoint'):
            import socket
            if not isinstance(self.endpoint, list): self.endpoint = [self.endpoint]
            for ep in self.endpoint:
                ep, port = ep if isinstance(ep, tuple) else (ep, ep.split(':')[1])
                hn,hp = ep.split(':')
                hn = socket.gethostbyname(hn)
                cmd += ['-p', f'{hn}:{hp}:{port}']
        # Image name
        if hasattr(self, 'image_name'):
            cmd += [self.image_name] if isinstance(self.image_name, str) else ['--platform', *self.image_name]
        else:
            cmd += [self.name]
        # Run command
        if command: cmd += [command]
        #
        if raw_cmd: return cmd
        run(cmd, msg=Text('Running docker image: ', self.name), or_else='')


    def push(self):
        cmd = ['docker', 'push', self.name]
        run(cmd, msg=Text(CLR.y, "Uploading~lang ja~アップロード", '... ', CLR.x),
            err=Text(print.ERR, 'Push failed. Try again after running: ~lang ja~プッシュに失敗した。 次のコマンドを実行した後、再試行してください。', 
                ['']*3, '   $ ', CLR.y, 'gcloud auth configure-docker asia.gcr.io', CLR.x))


    def label(self, key=None, default=None):
        l = json.loads(run(f'docker inspect {self.name}', msg='', read=True, or_else='[{"Config":{"Labels":{}}}]'))[0]['Config']['Labels']
        return l.get(key, default) if key else l


    def xensure_image(self, cfg, force_build=False, check_labels=True, check_branch=True, check_repos=True, abort_on_error=True):
        #proto = ProtoGen().autogen()
        cur_labels = {
            'target': cfg.target,
            'branch': Git('.').current_branch(),
        }
        cur_labels.update({'commit_'+r.name(): r.current_commit() for r in [Git(f'{COMMON_DIR}/{r}') for r in cfg.repos]})
        print.ln(CLR.y, "Labels:", CLR.x, ['']*2, [f"{k:>25} {CLR.a}{v}{CLR.x}" for k,v in cur_labels.items()])

        errors = []
        resolutions = []
        
        if check_branch and cur_labels['branch'] != cfg.docker_prefix:
            errors.append(Text(f'''
                Branch mismatch.  You are on `{cur_labels['branch']}`, but target `{cfg.target}` wants to be on branch `{cfg.docker_prefix}`'''))

        if check_repos:
            for r in cfg.repos:
                name = r.name()
                print.ln(f"Verifying `{name}` repo status~lang ja~{name}のリポジトリのステータスを確認する", '...')
                status = r.status()
                if status: 
                    errors.append(Text( f"`{CLR.y}{name}{CLR.x}` repo is not up to date", ['']*3, status
                        ))

        if check_labels and img_labels and not force_build:
            for k,v in cur_labels.items():
                if img_labels.get(k,'') != v:
                    errors.append(Text(f'''The image label `{CLR.y}{k}{CLR.x}` doesn't match the current source code.'''))

        if errors:
            print.ln(print.ERR if abort_on_error else print.WARN, "Current source configuration is inconsistant")
            for e in errors:
                print.ln(e)
            if abort_on_error: exit('Aborting...')

        if force_build or not img_labels:
            print.ln(CLR.y, "Building image... ", CLR.x, cfg.docker.name)
            cfg.docker.build(labels = cur_labels, nocache=force_build)
        else:
            print.ln(CLR.y, 'Exists: ', CLR.x, cfg.docker.name)
            


    def __str__(self):
        return f'{self.name}   [{self.lines[1]}]'


