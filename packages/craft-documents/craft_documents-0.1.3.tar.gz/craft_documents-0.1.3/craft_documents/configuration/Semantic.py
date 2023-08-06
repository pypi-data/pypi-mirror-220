from enum import Enum


class Semantic(Enum):
    """
    - OPTIONAL: `Resolve` will not be run.
    - REQUIRED: `Resolve` will be run.
    """

    OPTIONAL = 0
    REQUIRED = 1
