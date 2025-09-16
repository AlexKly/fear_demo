import os
import pathlib


_ROOT = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
DIR_SCREENSHOTS = _ROOT/'screenshots'
DIR_SCREEN = DIR_SCREENSHOTS/'screen'
DIR_WEBCAM = DIR_SCREENSHOTS/'webcam'
