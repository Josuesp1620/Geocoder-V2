from pathlib import Path

from geocode.config import config
from geocode.core.db import DB


@config.on_load
def load_scripts():
    root = Path(__file__).parent / "lua"
    for path in root.glob("*.lua"):
        with path.open() as f:
            name = path.name[:-4]
            globals()[name] = DB.register_script(f.read())
