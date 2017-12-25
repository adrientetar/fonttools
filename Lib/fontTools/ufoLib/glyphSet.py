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
            raise KeyError("name %s is not a string" % repr(glyph.name))
        fileName = self._contents.get[glyph.name]
        if fileName is None:
            # TODO: we could cache this to avoid recreating it for every glyph
            existing = set(name.lower() for name in self._contents.values())
            self._contents[glyph.name] = fileName = userNameToFileName(
                glyph.name, existing=existing, suffix=".glif")
        root = treeFromGlyph(glyph)
        tree = etree.ElementTree(root)
        path = os.path.join(self._path, fileName)
        with open(path, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)

    def writeLayerInfo(self, layer):
        layerDict = {
            "color": layer.color,
            "lib": layer.lib,
        }
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


def treeFromGlyph(glyph):
    root = etree.Element("glyph", {"name": glyph.name, "format": 3})
    treeFromOutline(glyph, etree.SubElement(root, "outline"))
    if glyph.width or glyph.height:
        advance = etree.SubElement(root, "advance")
        if glyph.width:
            advance.attrib["width"] = glyph.width
        if glyph.height:
            advance.attrib["height"] = glyph.height
    if glyph.unicodes:
        for value in glyph.unicodes:
            etree.SubElement(root, "unicode", {"hex": "%04X" % value})
    for anchor in glyph.anchors:
        attrs = {
            "x": anchor.x,
            "y": anchor.y,
        }
        if anchor.name is not None:
            attrs["name"] = anchor.name
        if anchor.color is not None:
            attrs["color"] = anchor.color
        if anchor.identifier is not None:
            attrs["identifier"] = anchor.identifier
        etree.SubElement(root, "anchor", attrs)
    for guideline in glyph.guidelines:
        attrs = {
            "x": guideline.x,
            "y": guideline.y,
            "angle": guideline.angle,
        }
        if guideline.name is not None:
            attrs["name"] = guideline.name
        if guideline.color is not None:
            attrs["color"] = guideline.color
        if guideline.identifier is not None:
            attrs["identifier"] = guideline.identifier
        etree.SubElement(root, "guideline", attrs)
    if glyph.image is not None:
        attrs = {
            "fileName": glyph.image.fileName,
            "xScale": glyph.image.transformation.xScale,
            "xyScale": glyph.image.transformation.xyScale,
            "yxScale": glyph.image.transformation.yxScale,
            "yScale": glyph.image.transformation.yScale,
            "xOffset": glyph.image.transformation.xOffset,
            "yOffset": glyph.image.transformation.yOffset,
        }
        if glyph.image.color is not None:
            attrs["color"] = glyph.image.color
        etree.SubElement(root, "image", attrs)
    if glyph.note:
        # TODO: indent etc.?
        etree.SubElement(root, "note", text=glyph.note)
    if glyph.lib:
        root.append(
            etree.fromstring(plistlib.dumps(glyph.lib)))
    return root


def treeFromOutline(glyph, outline):
    for contour in glyph.contours:
        element = etree.SubElement(outline, "contour")
        if contour.identifier is not None:
            element.attrib["identifier"] = contour.identifier
        for point in contour:
            attrs = {
                "x": point.x,
                "y": point.y,
                "type": point.type or "offcurve",
                "smooth": point.smooth,
            }
            if point.name is not None:
                attrs["name"] = point.name
            if point.identifier is not None:
                attrs["identifier"] = point.identifier
            etree.SubElement(element, "point", attrs)
    for component in glyph.components:
        attrs = {
            "base": component.baseGlyph,
            "xScale": component.transformation.xScale,
            "xyScale": component.transformation.xyScale,
            "yxScale": component.transformation.yxScale,
            "yScale": component.transformation.yScale,
            "xOffset": component.transformation.xOffset,
            "yOffset": component.transformation.yOffset,
        }
        if component.identifier is not None:
                attrs["identifier"] = component.identifier
        etree.SubElement(outline, "component", attrs)
