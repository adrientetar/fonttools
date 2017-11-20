import attr
# TODO: stop polluting here with these imports, make an object
# that holds all the classes and pass it from the reader
from fontTools.ufoLib.objects.anchor import Anchor
from fontTools.ufoLib.objects.component import Component
from fontTools.ufoLib.objects.contour import Contour
from fontTools.ufoLib.objects.glyph import Glyph
from fontTools.ufoLib.objects.guideline import Guideline
from fontTools.ufoLib.objects.image import Image
from fontTools.ufoLib.objects.point import Point
from lxml import etree
import os
import plistlib

CONTENTS_FILENAME = "contents.plist"


@attr.s(slots=True)
class GlyphSet(object):
    path = attr.ib(type=str)
    _contents = attr.ib(init=False, type=dict)

    def __attrs_post_init__(self):
        self.rebuildContents()

    def rebuildContents(self):
        path = os.path.join(self.path, CONTENTS_FILENAME)
        try:
            with open(path, "rb") as file:
                contents = plistlib.load(file)
        except FileNotFoundError:
            contents = {}
        # validate contents
        # ..
        self._contents = contents
        # self._reverseContents = None

    def readGlyph(self, name):
        fileName = self._contents[name]
        path = os.path.join(self.path, fileName)
        with open(path, "rb") as file:
            tree = etree.parse(file)
        # validate tree?
        # ..
        return glyphFromTree(tree.getroot())

    # dict

    def items(self):
        return self._contents.items()

    def keys(self):
        return self._contents.keys()

    def values(self):
        return self._contents.values()

    def __contains__(self, item):
        pass

    def __iter__(self):
        pass

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __len__(self):
        pass


_transformationInfo = (
    # field name, default value
    ("xScale",  1),
    ("xyScale", 0),
    ("yxScale", 0),
    ("yScale",  1),
    ("xOffset", 0),
    ("yOffset", 0),
)


def _number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def _transformation(element):
    transformation = []
    for ident, default in _transformationInfo:
        value = element.get(ident)
        if value is not None:
            value = _number(value)
        else:
            value = default
        transformation.append(value)
    return tuple(transformation)


def glyphFromTree(root):
    # XXX: pass custom classes
    # we could make a GlyphBuilder class instanciated
    # by the GlyphSet and pass a classes holder
    # UFOReader -> GlyphSet -> GlyphBuilder
    glyph = Glyph(root.attrib["name"])
    unicodes = []
    for element in root:
        if element.tag == "outline":
            outlineFromTree(element, glyph)
        elif element.tag == "advance":
            for key in ("width", "height"):
                if key in element.attrib:
                    setattr(glyph, key, _number(element.attrib[key]))
        elif element.tag == "unicode":
            unicodes.append(int(element.attrib["hex"], 16))
        elif element.tag == "anchor":
            anchor = Anchor(
                x=element.attrib["x"],
                y=element.attrib["y"],
                name=element.get("name"),
                # color
                identifier=element.get("identifier"),
            )
            glyph.appendAnchor(anchor)
        elif element.tag == "guideline":
            guideline = Guideline(
                x=element.get("x", 0),
                y=element.get("y", 0),
                angle=element.get("angle", 0),
                name=element.get("name"),
                # color
                identifier=element.get("identifier"),
            )
            glyph.appendGuideline(guideline)
        elif element.tag == "image":
            image = Image(
                fileName=element.attrib["fileName"],
                transformation=_transformation(element),
            )
            glyph.appendImage(image)
        elif element.tag == "note":
            # TODO: strip whitesp?
            glyph.note = element.text
        elif element.tag == "lib":
            glyph.lib = plistlib.loads(
                etree.tostring(element), fmt=plistlib.FMT_XML)
    glyph.unicodes = unicodes
    return glyph


def outlineFromTree(outline, glyph):
    for element in outline:
        if element.tag == "contour":
            contour = Contour()
            for element_ in element:
                segmentType = element_.attrib.get("type")
                # TODO: fallback to None like defcon or "offcurve"?
                if segmentType == "offcurve":
                    segmentType = None
                point = Point(
                    x=_number(element_.attrib["x"]),
                    y=_number(element_.attrib["y"]),
                    type=segmentType,
                    smooth=element_.attrib.get("smooth", False),
                    name=element_.get("name"),
                    identifier=element_.get("identifier"),
                )
                # TODO: collect and validate identifiers
                contour.append(point)
            glyph.appendContour(contour)
        elif element.tag == "component":
            component = Component(
                baseGlyph=element.attrib["base"],
                transformation=_transformation(element),
                identifier=element.get("identifier"),
            )
            glyph.appendComponent(component)
