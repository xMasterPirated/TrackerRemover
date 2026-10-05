import sys
import pystray
from PIL import Image
from pathlib import Path
from threading import Thread
from clipboard import keep_alive

def salir(icon, item):
    icon.stop()

if getattr(sys, "frozen", False): BASE_DIR = Path(sys.executable).parent
else: BASE_DIR = Path(__file__).parent
icon_file = BASE_DIR / "icon.ico"

imagen = Image.open(icon_file)
menu = pystray.Menu(pystray.MenuItem("Salir", salir))

icon = pystray.Icon("TrackerRemover", imagen, "Removing trackers from clipboard", menu)
Thread(target=keep_alive, daemon=True).start()
icon.run()