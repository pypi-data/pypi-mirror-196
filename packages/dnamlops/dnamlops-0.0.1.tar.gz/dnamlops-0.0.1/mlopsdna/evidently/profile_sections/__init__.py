import warnings

import mlopsdna.evidently as evidently.model_profile.sections
from mlopsdna.evidently.model_profile.sections import *

__path__ = evidently.model_profile.sections.__path__  # type: ignore

warnings.warn("'import mlopsdna.evidently as evidently.profile_sections' is deprecated, use 'import mlopsdna.evidently as evidently.model_profile.sections'")
