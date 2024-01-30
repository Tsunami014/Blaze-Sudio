import os

class LDtkAPP:
    def __init__(self):
        self.ldtkpath = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'ldtk', 'LDtk.exe')
        assert os.path.exists(self.ldtkpath), 'LDtk does not exist, or could not be found!' # TODO: make an installation for it

    def open(self, filepath):
        os.system(self.ldtkpath + ' -c "%s"'%filepath)
