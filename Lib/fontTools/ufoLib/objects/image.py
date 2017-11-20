import attr
from ._common import String


@attr.s(slots=True)
class Image(object):
    fileName = attr.ib(type=String)
    # TODO: need a more sophisticated validator here
    # len(6), Number
    # or make a special Transform type?
    transformation = attr.ib(type=tuple)
    color = attr.ib(default=None, type=String)
