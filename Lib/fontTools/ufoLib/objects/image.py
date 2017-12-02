import attr
from ._common import OptString
from fontTools.ufoLib.objects.misc import Transformation


@attr.s(slots=True)
class Image(object):
    fileName = attr.ib(type=OptString)
    transformation = attr.ib(type=Transformation)
    color = attr.ib(default=None, type=OptString)


OptImage = (Image, None)
