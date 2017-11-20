import attr
from fontTools.ufoLib.glyphSet import GlyphSet
import os
import plistlib

DEFAULT_GLYPHS_DIRNAME = "glyphs"

FEATURES_FILENAME = "features.plist"
FONTINFO_FILENAME = "fontinfo.plist"
LAYERCONTENTS_FILENAME = "layercontents.plist"

# TODO: color, dataSet, groups, kerning, imageSet, font.lib


@attr.s(slots=True)
class UFOReader(object):
    # TODO: we should probably take path-like objects, for zip etc. support.
    path = attr.ib(type=str)
    _layerContents = attr.ib(init=False, repr=False)

    # layers

    def getLayerContents(self):
        try:
            return self._layerContents
        except AttributeError:
            pass
        path = os.path.join(self.path, LAYERCONTENTS_FILENAME)
        with open(path, "rb") as file:
            # TODO: rewrite plistlib
            self._layerContents = plistlib.load(file)
        # TODO: check the data
        if self._layerContents:
            assert self._layerContents[0][1] == DEFAULT_GLYPHS_DIRNAME
        return self._layerContents

    def getGlyphSet(self, dirName):
        path = os.path.join(self.path, dirName)
        return GlyphSet(path)

    """
    def getDefaultLayerName(self):
        for name, dirName in self.getLayerContents():
            if dirName == DEFAULT_GLYPHS_DIRNAME:
                return name
        raise KeyError("no default directory was found")

    def getLayerNames(self):
        # layercontents should really be a dictionary
        return map(lambda l: l[0], self.getLayerContents())
    """

    # single reads

    def readFeatures(self):
        path = os.path.join(self.path, FEATURES_FILENAME)
        try:
            with open(path, "r") as file:
                text = file.read()
        except FileNotFoundError:
            text = ""
        return text

    def readInfo(self):
        path = os.path.join(self.path, FONTINFO_FILENAME)
        with open(path, "rb") as file:
            infoDict = plistlib.load(file)
        return infoDict
