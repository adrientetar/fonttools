from fontTools.ufoLib.objects.component import Component
from fontTools.ufoLib.objects.contour import Contour
from fontTools.ufoLib.objects.misc import Transformation
from fontTools.ufoLib.objects.point import Point
from fontTools.ufoLib.pointPens.basePen import AbstractPointPen


class GlyphPointPen(AbstractPointPen):
    __slots__ = "_glyph", "_contour"

    def __init__(self, glyph):
        self._glyph = glyph
        self._contour = None

    def beginPath(self, identifier=None, **kwargs):
        self._contour = Contour(identifier=identifier)

    def endPath(self):
        self._glyph.contours.append(self._contour)
        self._contour = None

    def addPoint(self, pt, **kwargs):
        kwargs["x"], kwargs["y"] = pt
        self._contour.append(Point(**kwargs))

    def addComponent(self, baseGlyph, transformation, **kwargs):
        transformation = Transformation(transformation)
        component = Component(baseGlyph, transformation, **kwargs)
        self._glyph.components.append(component)
