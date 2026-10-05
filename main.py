import pystray
from PIL import Image
from threading import Thread
from Clipboard import keep_alive

def salir(icon, item):
    icon.stop()

imagen = Image.open(r"C:\Users\Admin\Desktop\ChukTools\urltracker\icon.ico")
menu = pystray.Menu(pystray.MenuItem("Salir", salir))

icon = pystray.Icon("TrackerRemover", imagen, "Removing trackers from clipboard", menu)
Thread(target=keep_alive, daemon=True).start()
icon.run()