from appdirs import *
from pathlib import Path
from rich.console import Console
import os


__all__ = ("print",)

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"

# The folder needs to exist
if not USER_DIR.exists():
    USER_DIR.mkdir(parents=True)

# The file needs to exist to actually log something
if not LOG_FILE.exists():
    LOG_FILE.touch()

report_file = open(LOG_FILE, "wt", encoding="utf-8")

file_console = Console(file=report_file)

terminal_console = Console(color_system="truecolor" if os.name != "nt" else "windows")


def print(*args, **kwargs):
    file_console.print(*args, **kwargs)
    terminal_console.print(*args, **kwargs)
