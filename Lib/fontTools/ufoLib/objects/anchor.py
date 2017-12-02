import attr
from ._common import Number, OptString


@attr.s(slots=True)
class Anchor(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    name = attr.ib(default=None, type=OptString)
    color = attr.ib(default=None, type=OptString)
    identifier = attr.ib(default=None, type=OptString)
