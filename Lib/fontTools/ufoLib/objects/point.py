import attr
from ._common import Number, String


@attr.s(slots=True)
class Point(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    type = attr.ib(type=String)
    smooth = attr.ib(default=False, type=bool)
    name = attr.ib(default=None, type=String)
    identifier = attr.ib(default=None, type=String)
