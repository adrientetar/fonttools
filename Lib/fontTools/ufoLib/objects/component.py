import attr
from fontTools.ufoLib.objects.misc import Transformation
from fontTools.ufoLib.pointPens.converterPens import PointToSegmentPen
import warnings


@attr.s(slots=True)
class Component(object):
    baseGlyph = attr.ib(type=str)
    transformation = attr.ib(type=Transformation)
    identifier = attr.ib(default=None, type=str)

    # -----------
    # Pen methods
    # -----------

    def draw(self, pen):
        pointPen = PointToSegmentPen(pen)
        self.drawPoints(pointPen)

    def drawPoints(self, pointPen):
        try:
            pointPen.addComponent(self._baseGlyph, self._transformation, identifier=self.identifier)
        except TypeError:
            pointPen.addComponent(self._baseGlyph, self._transformation)
            warnings.warn("The addComponent method needs an identifier kwarg. The component's identifier value has been discarded.", UserWarning)
