import sys

if not str(sys.version).startswith("3"):
    # python 2 is literally a joke from the gods
    sys.stderr.write("Warning, crutil will likely fail on non-python 3 installations.\n")

from .metadata import *
from .crutil import *
