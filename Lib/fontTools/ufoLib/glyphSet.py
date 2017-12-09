import attr
from lxml import etree
import os
import plistlib

CONTENTS_FILENAME = "contents.plist"
LAYERINFO_FILENAME = "layerinfo.plist"

# Note: we can implement reporting with logging, and lxml Elements
# have a sourceline attr


@attr.s(slots=True)
class GlyphSet(object):
    _path = attr.ib(type=str)
    _contents = attr.ib(init=False, type=dict)

    def __attrs_post_init__(self):
        self.rebuildContents()

    @property
    def path(self):
        return self._path

    def rebuildContents(self):
        path = os.path.join(self._path, CONTENTS_FILENAME)
        try:
            with open(path, "rb") as file:
                contents = plistlib.load(file)
        except FileNotFoundError:
            contents = {}
        self._contents = contents

    def readGlyph(self, name, classes):
        fileName = self._contents[name]
        path = os.path.join(self._path, fileName)
        try:
            with open(path, "rb") as file:
                tree = etree.parse(file)
        except FileNotFoundError:
            raise KeyError(name)
        return glyphFromTree(tree.getroot(), classes)

    def readLayerInfo(self, layer):
        path = os.path.join(self._path, LAYERINFO_FILENAME)
        try:
            with open(path, "rb") as file:
                layerDict = plistlib.load(file)
        except FileNotFoundError:
            return
        for key, value in layerDict.items():
            setattr(layer, key, value)

    # dict

    def __contains__(self, name):
        return name in self._contents

    def __len__(self):
        return len(self._contents)

    def items(self):
        return self._contents.items()

    def keys(self):
        return self._contents.keys()

    def values(self):
        return self._contents.values()


def _number(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def _transformation(element, classes):
    return classes.Transformation(
        xScale=_number(element.get("xScale", 1)),
        xyScale=_number(element.get("xyScale", 0)),
        yxScale=_number(element.get("yxScale", 0)),
        yScale=_number(element.get("yScale", 1)),
        xOffset=_number(element.get("xOffset", 0)),
        yOffset=_number(element.get("yOffset", 0)),
    )


def glyphFromTree(root, classes):
    glyph = classes.Glyph(root.attrib["name"])
    unicodes = []
    for element in root:
        if element.tag == "outline":
            outlineFromTree(element, glyph, classes)
        elif element.tag == "advance":
            for key in ("width", "height"):
                if key in element.attrib:
                    setattr(glyph, key, _number(element.attrib[key]))
        elif element.tag == "unicode":
            unicodes.append(int(element.attrib["hex"], 16))
        elif element.tag == "anchor":
            anchor = classes.Anchor(
                x=_number(element.attrib["x"]),
                y=_number(element.attrib["y"]),
                name=element.get("name"),
                color=element.get("color"),
                identifier=element.get("identifier"),
            )
            glyph.anchors.append(anchor)
        elif element.tag == "guideline":
            guideline = classes.Guideline(
                x=_number(element.get("x", 0)),
                y=_number(element.get("y", 0)),
                angle=_number(element.get("angle", 0)),
                name=element.get("name"),
                color=element.get("color"),
                identifier=element.get("identifier"),
            )
            glyph.guidelines.append(guideline)
        elif element.tag == "image":
            image = classes.Image(
                fileName=element.attrib["fileName"],
                transformation=_transformation(element, classes),
                color=element.get("color"),
            )
            glyph.image = image
        elif element.tag == "note":
            # TODO: strip whitesp?
            glyph.note = element.text
        elif element.tag == "lib":
            glyph.lib = plistlib.loads(
                etree.tostring(element), fmt=plistlib.FMT_XML)
    glyph.unicodes = unicodes
    return glyph


def outlineFromTree(outline, glyph, classes):
    for element in outline:
        if element.tag == "contour":
            contour = classes.Contour(identifier=element.get("identifier"))
            for element_ in element:
                pointType = element_.get("type")
                # TODO: fallback to None like defcon or "offcurve"?
                if pointType == "offcurve":
                    pointType = None
                point = classes.Point(
                    x=_number(element_.attrib["x"]),
                    y=_number(element_.attrib["y"]),
                    type=pointType,
                    smooth=element_.get("smooth", False),
                    name=element_.get("name"),
                    identifier=element_.get("identifier"),
                )
                contour.append(point)
            glyph.contours.append(contour)
        elif element.tag == "component":
            component = classes.Component(
                baseGlyph=element.attrib["base"],
                transformation=_transformation(element, classes),
                identifier=element.get("identifier"),
            )
            glyph.components.append(component)
