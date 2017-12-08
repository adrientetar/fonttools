import attr
from fontTools.ufoLib.glyphSet import GlyphSet
import os
import plistlib

DATA_DIRNAME = "data"
DEFAULT_GLYPHS_DIRNAME = "glyphs"
IMAGES_DIRNAME = "images"

FEATURES_FILENAME = "features.plist"
FONTINFO_FILENAME = "fontinfo.plist"
GROUPS_FILENAME = "groups.plist"
KERNING_FILENAME = "kerning.plist"
LAYERCONTENTS_FILENAME = "layercontents.plist"
LIB_FILENAME = "lib.plist"


@attr.s(slots=True)
class UFOReader(object):
    # TODO: we should probably take path-like objects, for zip etc. support.
    _path = attr.ib(type=str)
    _layerContents = attr.ib(init=False, repr=False, type=list)

    @property
    def path(self):
        return self._path

    def getDataDirectoryListing(self, maxDepth=24):
        path = os.path.join(self._path, DATA_DIRNAME)
        return self._getDirectoryListing(path, maxDepth=maxDepth)

    def _getDirectoryListing(self, path, depth=0, maxDepth=24):
        if depth > maxDepth:
            # should we just silently return here?
            raise RuntimeError("Maximum depth reached: %s" % maxDepth)
        files = []
        try:
            listdir = os.listdir(path)
        except FileNotFoundError:
            return files
        for fileName in listdir:
            f = os.path.join(path, fileName)
            if os.path.isdir(f):
                files.extend(self._getDirectoryListing(f, depth=depth+1, maxDepth=maxDepth))
            else:
                relPath = os.path.relPath(f, self._path)
                files.append(relPath)
        return relPath

    def getImageDirectoryListing(self):
        path = os.path.join(self._path, IMAGES_DIRNAME)
        files = []
        try:
            listdir = os.listdir(path)
        except FileNotFoundError:
            return files
        for fileName in listdir:
            f = os.path.join(path, fileName)
            if os.path.isdir(f):
                continue
            files.append(fileName)
        return files

    # layers

    def getLayerContents(self):
        try:
            return self._layerContents
        except AttributeError:
            pass
        path = os.path.join(self._path, LAYERCONTENTS_FILENAME)
        with open(path, "rb") as file:
            # TODO: rewrite plistlib
            self._layerContents = plistlib.load(file)
        # TODO: check the data
        if self._layerContents:
            assert self._layerContents[0][1] == DEFAULT_GLYPHS_DIRNAME
        return self._layerContents

    def getGlyphSet(self, dirName):
        path = os.path.join(self._path, dirName)
        return GlyphSet(path)

    # single reads

    def readData(self, fileName):
        path = os.path.join(self._path, DATA_DIRNAME, fileName)
        try:
            with open(path, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            data = None
        return data

    def readImage(self, fileName):
        path = os.path.join(self._path, IMAGES_DIRNAME, fileName)
        try:
            with open(path, "rb") as file:
                data = file.read()
        except FileNotFoundError:
            data = None
        return data

    def readFeatures(self):
        path = os.path.join(self._path, FEATURES_FILENAME)
        try:
            with open(path, "r") as file:
                text = file.read()
        except FileNotFoundError:
            text = ""
        return text

    def readGroups(self):
        path = os.path.join(self._path, GROUPS_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readInfo(self):
        path = os.path.join(self._path, FONTINFO_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readKerning(self):
        path = os.path.join(self._path, KERNING_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def readLib(self):
        path = os.path.join(self._path, LIB_FILENAME)
        try:
            with open(path, "rb") as file:
                data = plistlib.load(file)
        except FileNotFoundError:
            data = {}
        return data
