import warnings

import mlopsdna.evidently as evidently.dashboard.tabs
from mlopsdna.evidently.dashboard.tabs import *

__path__ = evidently.dashboard.tabs.__path__  # type: ignore

warnings.warn("'import mlopsdna.evidently as evidently.tabs' is deprecated, use 'import mlopsdna.evidently as evidently.dashboard.tabs'")
