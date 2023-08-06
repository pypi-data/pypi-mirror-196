from pathlib import Path

# Paths
HOME = Path.home()
FILES = HOME / ".gintel"
CACHE = FILES / "cache"
TOKENS = f"{FILES}/tokens.json"

# Data
TTC_MAP = {"NW": [0, 0], "NE": [1, 0], "SW": [0, 1], "SE": [1, 1], "CE": [0.5, 0.5]}
