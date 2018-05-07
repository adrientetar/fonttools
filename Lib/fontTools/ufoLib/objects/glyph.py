import attr
from fontTools.ufoLib.objects.anchor import Anchor
from fontTools.ufoLib.objects.component import Component
from fontTools.ufoLib.objects.contour import Contour
from fontTools.ufoLib.objects.guideline import Guideline
from fontTools.ufoLib.objects.image import Image
from fontTools.ufoLib.objects.misc import Transformation
from fontTools.ufoLib.objects.point import Point
from fontTools.ufoLib.pointPens.converterPens import PointToSegmentPen, SegmentToPointPen
from fontTools.ufoLib.pointPens.glyphPointPen import GlyphPointPen
from typing import Optional, Union


@attr.s(slots=True)
class Glyph(object):
    _name = attr.ib(type=str)
    width = attr.ib(default=0, init=False, type=Union[int, float])
    height = attr.ib(default=0, init=False, type=Union[int, float])
    unicodes = attr.ib(default=attr.Factory(list), init=False, type=list)

    image = attr.ib(default=None, init=False, repr=False, type=Optional[Image])
    lib = attr.ib(default=attr.Factory(dict), init=False, repr=False, type=dict)
    note = attr.ib(default=None, init=False, repr=False, type=Optional[str])

    anchors = attr.ib(default=attr.Factory(list), init=False, repr=False, type=list)
    components = attr.ib(default=attr.Factory(list), init=False, repr=False, type=list)
    contours = attr.ib(default=attr.Factory(list), init=False, repr=False, type=list)
    guidelines = attr.ib(default=attr.Factory(list), init=False, repr=False, type=list)

    @property
    def name(self):
        return self._name

    @property
    def unicode(self):
        if self.unicodes:
            return self.unicodes[0]
        return None

    @unicode.setter
    def unicode(self, value):
        if value is None:
            self.unicodes = []
        else:
            if self.unicodes[0] == value:
                return
            try:
                self.unicodes.remove(value)
            except ValueError:
                pass
            self.unicodes.insert(0, value)

    def clear(self):
        self.anchors = []
        self.components = []
        self.contours = []
        self.guidelines = []
        self.image = None

    # -----------
    # Pen methods
    # -----------

    def draw(self, pen):
        pointPen = PointToSegmentPen(pen)
        self.drawPoints(pointPen)

    def drawPoints(self, pointPen):
        for contour in self.contours:
            contour.drawPoints(pointPen)
        for component in self.components:
            component.drawPoints(pointPen)

    def getPen(self):
        pen = SegmentToPointPen(self.getPointPen())
        return pen

    def getPointPen(self):
        pointPen = GlyphPointPen(self)
        return pointPen


class GlyphClasses(object):
    Anchor = Anchor
    Component = Component
    Contour = Contour
    Glyph = Glyph
    Guideline = Guideline
    Image = Image
    Point = Point

    Transformation = Transformation
