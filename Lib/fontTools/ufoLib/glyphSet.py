import attr
from fontTools.ufoLib.constants import (
    CONTENTS_FILENAME, LAYERINFO_FILENAME)
from lxml import etree
import os
import plistlib
from ufoLib.filenames import userNameToFileName  # XXX fonttools

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

    # r

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

    # w

    def deleteGlyph(self, name):
        fileName = self._contents[name]
        path = os.path.join(self._path, fileName)
        os.remove(path)
        del self._contents[name]

    def writeContents(self):
        path = os.path.join(self._path, CONTENTS_FILENAME)
        with open(path, "wb") as file:
            plistlib.dump(self._contents, file)

    def writeGlyph(self, glyph):
        if not glyph.name:
            raise KeyError("name %r is not a string" % glyph.name)
        fileName = self._contents.get(glyph.name)
        if fileName is None:
            # TODO: we could cache this to avoid recreating it for every glyph
            existing = set(name.lower() for name in self._contents.values())
            self._contents[glyph.name] = fileName = userNameToFileName(
                glyph.name, existing=existing, suffix=".glif")
        root = treeFromGlyph(glyph)
        tree = etree.ElementTree(root)
        path = os.path.join(self._path, fileName)
        with open(path, "wb") as file:
            tree.write(file, encoding="utf-8", pretty_print=True, xml_declaration=True)

    def writeLayerInfo(self, layer):
        layerDict = {}
        if layer.color is not None:
            layerDict["color"] = layer.color
        if layer.lib:
            layerDict["lib"] = layer.lib
        path = os.path.join(self._path, LAYERINFO_FILENAME)
        with open(path, "wb") as file:
            plistlib.dump(layerDict, file)

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


def _transformation_back(transformation, d):
    if transformation.xScale != 1:
        d["xScale"] = repr(transformation.xScale)
    if transformation.xyScale != 0:
        d["xyScale"] = repr(transformation.xyScale)
    if transformation.yxScale != 0:
        d["yxScale"] = repr(transformation.yxScale)
    if transformation.yScale != 1:
        d["yScale"] = repr(transformation.yScale)
    if transformation.xOffset != 0:
        d["xOffset"] = repr(transformation.xOffset)
    if transformation.yOffset != 0:
        d["yOffset"] = repr(transformation.yOffset)


def glyphFromTree(root, classes):
    glyph = classes.Glyph(root.attrib["name"])
    unicodes = []
    for element in root:
        if element.tag == "advance":
            for key in ("width", "height"):
                if key in element.attrib:
                    setattr(glyph, key, _number(element.attrib[key]))
        elif element.tag == "unicode":
            unicodes.append(int(element.attrib["hex"], 16))
        elif element.tag == "note":
            # TODO: strip whitesp?
            glyph.note = element.text
        elif element.tag == "image":
            image = classes.Image(
                fileName=element.attrib["fileName"],
                transformation=_transformation(element, classes),
                color=element.get("color"),
            )
            glyph.image = image
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
        elif element.tag == "anchor":
            anchor = classes.Anchor(
                x=_number(element.attrib["x"]),
                y=_number(element.attrib["y"]),
                name=element.get("name"),
                color=element.get("color"),
                identifier=element.get("identifier"),
            )
            glyph.anchors.append(anchor)
        elif element.tag == "outline":
            outlineFromTree(element, glyph, classes)
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


def treeFromGlyph(glyph):
    root = etree.Element("glyph", {"name": glyph.name, "format": repr(2)})
    # advance
    if glyph.width or glyph.height:
        advance = etree.SubElement(root, "advance")
        if glyph.width:
            advance.attrib["width"] = repr(glyph.width)
        if glyph.height:
            advance.attrib["height"] = repr(glyph.height)
    # unicodes
    if glyph.unicodes:
        for value in glyph.unicodes:
            etree.SubElement(root, "unicode", {"hex": "%04X" % value})
    # note
    if glyph.note:
        # TODO: indent etc.?
        etree.SubElement(root, "note", text=glyph.note)
    # image
    if glyph.image is not None:
        attrs = {
            "fileName": glyph.image.fileName,
        }
        _transformation_back(glyph.image.transformation, attrs)
        if glyph.image.color is not None:
            attrs["color"] = glyph.image.color
        etree.SubElement(root, "image", attrs)
    # guidelines
    for guideline in glyph.guidelines:
        attrs = {
            "x": repr(guideline.x),
            "y": repr(guideline.y),
            "angle": repr(guideline.angle),
        }
        if guideline.name is not None:
            attrs["name"] = guideline.name
        if guideline.color is not None:
            attrs["color"] = guideline.color
        if guideline.identifier is not None:
            attrs["identifier"] = guideline.identifier
        etree.SubElement(root, "guideline", attrs)
    # anchors
    for anchor in glyph.anchors:
        attrs = {
            "x": repr(anchor.x),
            "y": repr(anchor.y),
        }
        if anchor.name is not None:
            attrs["name"] = anchor.name
        if anchor.color is not None:
            attrs["color"] = anchor.color
        if anchor.identifier is not None:
            attrs["identifier"] = anchor.identifier
        etree.SubElement(root, "anchor", attrs)
    # outline
    treeFromOutline(glyph, etree.SubElement(root, "outline"))
    # lib
    if glyph.lib:
        lib = etree.SubElement(root, "lib")
        plist = etree.fromstring(plistlib.dumps(glyph.lib))
        lib.append(plist[0])
    return root


def treeFromOutline(glyph, outline):
    for contour in glyph.contours:
        element = etree.SubElement(outline, "contour")
        if contour.identifier is not None:
            element.attrib["identifier"] = contour.identifier
        for point in contour:
            attrs = {
                "x": repr(point.x),
                "y": repr(point.y),
            }
            if point.type is not None:
                attrs["type"] = point.type
            if point.smooth:
                attrs["smooth"] = "yes"
            if point.name is not None:
                attrs["name"] = point.name
            if point.identifier is not None:
                attrs["identifier"] = point.identifier
            etree.SubElement(element, "point", attrs)
    for component in glyph.components:
        attrs = {
            "base": component.baseGlyph,
        }
        _transformation_back(component.transformation, attrs)
        if component.identifier is not None:
                attrs["identifier"] = component.identifier
        etree.SubElement(outline, "component", attrs)
