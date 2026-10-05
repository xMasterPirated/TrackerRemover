import subprocess
import sys
from pathlib import Path

SCRIPT = "main.py"
NAME = "TrackerRemover"
ICON = "icon.ico"

BASE_DIR = Path(__file__).parent

def main():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "pyinstaller"
        ])

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--noconsole",
        "--clean",
        "--name", NAME,

        "--add-data",
        f"{BASE_DIR / 'trackers'};.",

        "--add-data",
        f"{BASE_DIR / 'icon.ico'};.",

        "--icon",
        str(BASE_DIR / "icon.ico"),

        str(BASE_DIR / SCRIPT),
    ]

    subprocess.check_call(command)

    print("\nBuild completed!")
    print(f"Executable: {BASE_DIR / 'dist' / (NAME + '.exe')}")

    input("\nPress Enter to close...")


if __name__ == "__main__":
    main()