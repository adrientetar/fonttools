import attr
from ._common import Number, OptString


@attr.s(slots=True)
class Guideline(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    angle = attr.ib(type=Number)
    name = attr.ib(default=None, type=OptString)
    color = attr.ib(default=None, type=OptString)
    identifier = attr.ib(default=None, type=OptString)
