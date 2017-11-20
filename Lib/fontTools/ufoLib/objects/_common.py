from enum import Enum, auto  # py3 only

Number = (int, float)
String = (str, None)


class PointTypes(Enum):
    MOVE = auto()
    LINE = auto()
    OFFCURVE = auto()
    CURVE = auto()
    QCURVE = auto()
