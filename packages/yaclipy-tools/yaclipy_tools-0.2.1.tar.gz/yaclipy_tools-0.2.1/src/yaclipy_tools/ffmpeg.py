from .sys_tool import SysTool

class FFmpeg(SysTool):
    exe = ('CMD_FFMPEG', 'ffmpeg')
    ver = '5.1'

    def version(self):
        v = run([self.exe, '-version'], capture_output=True).stdout.decode('utf-8').splitlines()[0]
        return list(map(int, v.split(' ')[2].split('.')))
    
    
    def cmd(self, infile, outfile, *args):
       return [self.exe, '-y', '-i', infile] + list(args) + [outfile]
        
        
    def run(self, infile, outfile, *args, verbose=False):
        cmd = self.cmd(infile, outfile, *args)
        (log.info if verbose else log.debug)(' '.join(cmd))
        c = run(cmd, capture_output=(not verbose))
        assert(c.returncode == 0), f"ffmpeg error\n{c.stderr.decode('utf8')}"
