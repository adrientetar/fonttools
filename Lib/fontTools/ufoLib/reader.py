import attr
from fontTools.ufoLib.glyphSet import GlyphSet
import os
import plistlib

DEFAULT_GLYPHS_DIRNAME = "glyphs"

FEATURES_FILENAME = "features.plist"
FONTINFO_FILENAME = "fontinfo.plist"
GROUPS_FILENAME = "groups.plist"
KERNING_FILENAME = "kerning.plist"
LAYERCONTENTS_FILENAME = "layercontents.plist"
LIB_FILENAME = "lib.plist"

# TODO: dataSet, imageSet


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

    # single reads

    def readFeatures(self):
        path = os.path.join(self.path, FEATURES_FILENAME)
        try:
            with open(path, "r") as file:
                text = file.read()
        except FileNotFoundError:
            text = ""
        return text

    def readGroups(self):
        path = os.path.join(self.path, GROUPS_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readInfo(self):
        path = os.path.join(self.path, FONTINFO_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readKerning(self):
        path = os.path.join(self.path, KERNING_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readLib(self):
        path = os.path.join(self.path, LIB_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data
