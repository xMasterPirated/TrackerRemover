import sys
import pystray
from PIL import Image
from pathlib import Path
from threading import Thread
from clipboard import keep_alive

def resource_path(filename):
    if getattr(sys, "frozen", False): return Path(sys._MEIPASS) / filename
    return Path(__file__).resolve().parent / filename

def salir(icon, item):
    icon.stop()

icon_image = Image.open(resource_path("icon.ico"))
menu = pystray.Menu(pystray.MenuItem("Salir", salir))
icon = pystray.Icon("TrackerRemover", icon_image, "Removing trackers from clipboard", menu)
Thread(target=keep_alive, daemon=True).start()
icon.run()