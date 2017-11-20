import attr
from ._common import Number, String


@attr.s(slots=True)
class Anchor(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    name = attr.ib(default=None, type=String)
    color = attr.ib(default=None, type=String)
    identifier = attr.ib(default=None, type=String)
