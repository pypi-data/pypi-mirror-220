from .old import Old
from .frmnc import Frmnc
from .frmnc666 import Frmnc666
from .cs141 import Cs141
from .gden_nt07 import GdenNt07

__version__ = '0.0.2'

KINDS = {
    'old': Old,
    'frmnc': Frmnc,
    'frmnc666': Frmnc666,
    'cs141': Cs141,
    'gden-nt07': GdenNt07,
}
