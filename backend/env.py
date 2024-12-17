import os
from pathlib import Path


APP_DIR = Path(__file__).parent  # the path containing this file
print(APP_DIR)
BASE_DIR = APP_DIR.parent  # the path containing the app directory

ENV = os.environ.get("ENV", "dev")

####################################
# DATA/FRONTEND BUILD DIR
####################################

DATA_DIR = Path(os.getenv("DATA_DIR", APP_DIR / "data")).resolve()
STATIC_DIR = Path(os.getenv("STATIC_DIR", APP_DIR / "static"))
CACHE_DIR = Path(os.getenv("CACHE_DIR", APP_DIR / "cache"))
FRONTEND_BUILD_DIR = Path(os.getenv("FRONTEND_BUILD_DIR", BASE_DIR / "build")).resolve()
