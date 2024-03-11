import os, subprocess, win32gui, win32com.client, pythoncom, win32con
from threading import Thread

class LDtkAPP:
    def __init__(self):
        self.ldtkpath = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'ldtk', 'LDtk.exe')
        assert os.path.exists(self.ldtkpath), 'LDtk does not exist, or could not be found!' # TODO: make an installation for it
        self.process, self.findWinThread, self.win = None, None, None
        self.killed = False
    
    def _get_window(self):
        self.win = None
        self.killed = False
        while self.win is None and not self.killed:
            def winEnumHandler(hwnd, ctx):
                if win32gui.IsWindowVisible(hwnd):
                    txt = win32gui.GetWindowText(hwnd)
                    if 'LDtk' in txt and 'LDtk' != txt: # Find the LDtk application that has FINISHED loading
                        self.win = hwnd
            win32gui.EnumWindows(winEnumHandler, None)
        if self.win is not None:
            self.focusWIN()
            self.make_full()
    
    def not_max(self):
        tup = win32gui.GetWindowPlacement(self.win)
        return tup[1] == win32con.SW_SHOWNORMAL
    
    def make_full(self):
        if self.not_max():
            #win32gui.MoveWindow(self.win, 0, 0, 99999999, 99999999, True)
            win32gui.ShowWindow(self.win, win32con.SW_MAXIMIZE)
    
    def focusWIN(self):
        if self.win is None:
            raise ValueError(
                'LDtk has not been launched, or you have not found it yet!'
            )
        pythoncom.CoInitialize() 
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys(' ') #Undocks my focus from wherever it may be
        # Another answer said to use shell.SendKeys('%'), but... This works better
        win32gui.SetForegroundWindow(self.win)
    
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
        self.kill = True
        self.win = None

    def open(self, filepath):
        self.process = subprocess.Popen([self.ldtkpath, '-c:"%s"'%filepath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.findWinThread = Thread(target=self._get_window, daemon=True)
        self.findWinThread.start()
    
    def is_win_open(self):
        return self.win is not None and bool(win32gui.IsWindow(self.win))

    def wait_for_win(self):
        while self.win is None: pass
