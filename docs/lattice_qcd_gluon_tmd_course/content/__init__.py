"""课程内容分卷。"""

from .foundations import VOLUMES as FOUNDATION_VOLUMES
from .lattice import VOLUMES as LATTICE_VOLUMES
from .partons import VOLUMES as PARTON_VOLUMES
from .implementation import VOLUMES as IMPLEMENTATION_VOLUMES
from .advanced import VOLUMES as ADVANCED_VOLUMES

VOLUMES = (
    *FOUNDATION_VOLUMES,
    *LATTICE_VOLUMES,
    *PARTON_VOLUMES,
    *IMPLEMENTATION_VOLUMES,
    *ADVANCED_VOLUMES,
)

__all__ = ["VOLUMES"]
