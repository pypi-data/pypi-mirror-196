import warnings

import mlopsdna.evidently as evidently.dashboard.widgets
from mlopsdna.evidently.dashboard.widgets import *

__path__ = evidently.dashboard.widgets.__path__  # type: ignore

warnings.warn("'import mlopsdna.evidently as evidently.widgets' is deprecated, use 'import mlopsdna.evidently as evidently.dashboard.widgets'")
