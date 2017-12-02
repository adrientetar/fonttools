import attr
from ._common import Number


@attr.s(slots=True)
class Transformation(object):
    xScale = attr.ib(default=1, type=Number)
    xyScale = attr.ib(default=0, type=Number)
    yxScale = attr.ib(default=0, type=Number)
    yScale = attr.ib(default=1, type=Number)
    xOffset = attr.ib(default=0, type=Number)
    yOffset = attr.ib(default=0, type=Number)

    # getitem, len?
    # algebra ops?
    # translate, shear, skew, etc.?
    #
    # iter lets us create a tuple
    #
    # Qt QTransform methods should be a good reference
    # e.g. inverted() makes a copy, like reversed() for py iterators

    def __iter__(self):
        yield self.xScale
        yield self.xyScale
        yield self.yxScale
        yield self.yScale
        yield self.xOffset
        yield self.yOffset

    # translate?
    def move(self, dx, dy):
        self.xOffset += dx
        self.yOffset += dy
