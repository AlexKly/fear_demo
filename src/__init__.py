import os
import pathlib

from src.utils import files


# Paths:
_ROOT = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
DIR_SCREENSHOTS = _ROOT/'screenshots'
DIR_SCREEN = DIR_SCREENSHOTS/'screen'
DIR_WEBCAM = DIR_SCREENSHOTS/'webcam'

# Make dirs:
files.mkdir(path=DIR_SCREENSHOTS)
files.mkdir(path=DIR_SCREEN)
files.mkdir(path=DIR_WEBCAM)
