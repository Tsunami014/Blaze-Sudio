import os, subprocess, platform
from tkinter.filedialog import askopenfilename
from threading import Thread

class LDtkAPP:
    def __init__(self):
        self.ldtkpath = None
        if platform.system() == 'Windows':
            self.ldtkpath = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'ldtk', 'LDtk.exe')
        elif platform.system() == 'Linux':
            if os.path.exists(os.path.join(os.getenv('HOME'), 'Applications')):
                for i in os.listdir(os.path.join(os.getenv('HOME'), 'Applications')):
                    if 'ldtk' in i.lower():
                        self.ldtkpath = os.path.join(os.getenv('HOME'), 'Applications', i)
                        break
            if self.ldtkpath is None:
                self.ldtkpath = askopenfilename(filetypes=[('Appimage files', ['.Appimage'])], initialdir=os.getenv('HOME'))
        else:
            raise ValueError(
                f'Platform {platform.system()} is not supported! Only supported: Windows and Linux.'
            )
        # TODO: Make LDtk not required for this to run
        assert os.path.exists(self.ldtkpath), 'LDtk does not exist, or could not be found!' # TODO: make an installation for it
        self.process = None
    
    def launch(self):
        self.process = subprocess.Popen([self.ldtkpath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.findWinThread = Thread(target=self._get_window, daemon=True)
        self.findWinThread.start()
    
    def kill(self):
        if self.process is None:
            raise ValueError(
                'LDtk is not running!'
            )
        self.process.kill()

    def open(self, filepath):
        self.process = subprocess.Popen([self.ldtkpath, '-c:"%s"'%filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.findWinThread = Thread(target=self._get_window, daemon=True)
        self.findWinThread.start()
