from importlib.resources import files

# Paths to package data files.
BASE_DIR = files('BlazeSudio') / 'graphics/GUI/textboxify'
DATA_DIR = BASE_DIR / 'data'
BORDER_DIR = DATA_DIR / "border"
INDICATOR_DIR = DATA_DIR / "indicator"
PORTRAIT_DIR = DATA_DIR / "portrait"

# Default sprite files.
DEFAULT_INDICATOR = {
    "file": INDICATOR_DIR / "idle.png",
    "size": (25, 17),
}
DEFAULT_PORTRAIT = {
    "file": PORTRAIT_DIR / "placeholder.png",
    "size": (100, 100),
}
