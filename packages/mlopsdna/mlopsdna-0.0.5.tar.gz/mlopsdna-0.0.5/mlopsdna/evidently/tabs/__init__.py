import warnings

import mlopsdna.evidently.dashboard.tabs
from mlopsdna.evidently.dashboard.tabs import *

__path__ = evidently.dashboard.tabs.__path__  # type: ignore

warnings.warn("'import mlopsdna.evidently.tabs' is deprecated, use 'import mlopsdna.evidently.dashboard.tabs'")
