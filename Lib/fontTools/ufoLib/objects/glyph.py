import attr
from ._common import Number


# TODO: look at attrs converters

@attr.s(slots=True)
class Glyph(object):
    name = attr.ib(type=str)
    width = attr.ib(init=False, type=Number)
    height = attr.ib(init=False, type=Number)
    unicodes = attr.ib(init=False, type=list)
    lib = attr.ib(init=False, repr=False, type=dict)
    _anchors = attr.ib(init=False, repr=False, type=list)
    _components = attr.ib(init=False, repr=False, type=list)
    _contours = attr.ib(init=False, repr=False, type=list)
    _guidelines = attr.ib(init=False, repr=False, type=list)

    def __attrs_post_init__(self):
        self.width = 0
        self.height = 0
        self.unicodes = []
        self.lib = []
        # TODO: make these lazy?
        self._anchors = []
        self._components = []
        self._contours = []
        self._guidelines = []

    @property
    def unicode(self):
        if self.unicodes:
            return self.unicodes[0]
        return None

    def appendAnchor(self, anchor):
        self._anchors.append(anchor)

    def appendComponent(self, component):
        self._components.append(component)

    def appendContour(self, contour):
        self._contours.append(contour)

    def appendGuideline(self, guideline):
        self._guidelines.append(guideline)
