

class FileSet(list):
    def add(self, name, flags=0):
        if name.startswith('members/') or name in ['.gitignore', 'README.rst']: return
        f = self.get(name)         
        if name.endswith('.gpg') or name.endswith('.orig'):
            flags |= File.NOEXIST | (File.GPG if name.endswith('.gpg') else File.CONFLICT)
        if not f:
            f.flags = flags
            self.append(f)
        else:
            f.flags = (f.flags|flags) & (0xff^File.NOEXIST)

    def get(self, name):
        n, ext = os.path.splitext(str(name))
        if ext in ['.gpg', '.orig']: name = n
        if name in self: return self[self.index(name)]
        return File(name, -1)



