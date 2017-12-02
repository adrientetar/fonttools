import attr
from ._common import Number, OptString


@attr.s(slots=True)
class Point(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    type = attr.ib(type=OptString)
    smooth = attr.ib(default=False, type=bool)
    name = attr.ib(default=None, type=OptString)
    identifier = attr.ib(default=None, type=OptString)
