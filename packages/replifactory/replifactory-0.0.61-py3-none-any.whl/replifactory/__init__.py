# if python version is less than 3.8, importlib.metadata is not available
# so     we use importlib_metadata instead
try:
    import importlib.metadata

    __version__ = importlib.metadata.version("replifactory")
except ImportError:
    import importlib_metadata as importlib_metadata

    __version__ = importlib_metadata.version("replifactory")

import subprocess
import sys

# from .device.base_device import BaseDevice
# from .device.morbidostat_device import MorbidostatDevice
# from .culture import TurbidostatCulture, MorbidostatCulture
from IPython.display import display

_main_gui = None


def upgrade_replifactory():
    """Upgrade the replifactory package to the latest version on PyPI"""
    print("upgrading replifactory...")
    output = subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "--upgrade", "replifactory"]
    )
    print(output.decode("utf-8"))


def gui():
    """
    Launch the replifactory GUI in a Jupyter notebook
    """
    from .GUI.main_gui import MainGuiBuilder

    global _main_gui
    if _main_gui is None:
        _main_gui = MainGuiBuilder()

    display(_main_gui.widget)
