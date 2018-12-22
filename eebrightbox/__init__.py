"""
Init.
"""

from . import core
from .errors import (
    EEBrightBoxException,
    AuthenticationException,
)

# aliases
EEBrightBox = core.EEBrightBox
