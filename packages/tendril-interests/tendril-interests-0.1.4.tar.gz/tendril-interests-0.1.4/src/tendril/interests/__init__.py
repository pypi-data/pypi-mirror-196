from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .manager import InterestManager
_manager = InterestManager(prefix='tendril.interests')

import sys
sys.modules[__name__] = _manager
_manager.finalize()
