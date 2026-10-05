import ctypes
import win32con
import win32gui
import win32clipboard

from url_manager import find_urls, remove_trackers

user32 = ctypes.windll.user32
WM_CLIPBOARDUPDATE = 0x031D

class ClipboardWatcher:
    def __init__(self):
        self.hwnd = None
        self.changing_clipboard = False
        self.cache = {}

    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        try:
            if not win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT): return None
            return win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)

        finally: win32clipboard.CloseClipboard()

    def set_clipboard(self, text):
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
        finally: win32clipboard.CloseClipboard()

    def on_clipboard_change(self):
        if self.changing_clipboard: return
        text = self.get_clipboard()
        if text is None: return

        urls = find_urls(text)
        if not urls: return
        new_text = str(text)

        for url in urls:
            if url in self.cache: new_text = new_text.replace(url, self.cache[url])
            else:
                nurl = remove_trackers(url)
                self.cache[url] = nurl
                if nurl == url: continue
                new_text = new_text.replace(url, nurl)

        if new_text == text: return        
        self.changing_clipboard = True
        try: self.set_clipboard(new_text)
        finally: self.changing_clipboard = False

    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_CLIPBOARDUPDATE:
            self.on_clipboard_change()
            return 0

        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0

        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def start(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "ClipboardWatcher"

        class_atom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(class_atom, "Clipboard Watcher", 0, 0, 0, 0, 0, 0, 0, 0, None)
        user32.AddClipboardFormatListener.argtypes = [ctypes.c_void_p]
        user32.AddClipboardFormatListener.restype = ctypes.c_bool

        if not user32.AddClipboardFormatListener(self.hwnd): raise ctypes.WinError()
        win32gui.PumpMessages()

def keep_alive():
    watcher = ClipboardWatcher()
    watcher.start()