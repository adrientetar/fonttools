import attr
from fontTools.ufoLib.objects.misc import Transformation
from typing import Optional


@attr.s(slots=True)
class Image(object):
    fileName = attr.ib(type=Optional[str])
    transformation = attr.ib(type=Transformation)
    color = attr.ib(default=None, type=Optional[str])
