import attr
from fontTools.ufoLib.constants import (
    DATA_DIRNAME, FEATURES_FILENAME, FONTINFO_FILENAME, GROUPS_FILENAME,
    KERNING_FILENAME, IMAGES_DIRNAME, LAYERCONTENTS_FILENAME, LIB_FILENAME)
from fontTools.ufoLib.glyphSet import GlyphSet
import os
import plistlib
import shutil
from ufoLib.filenames import userNameToFileName  # XXX fonttools


@attr.s(slots=True)
class UFOWriter(object):
    # TODO: we should probably take path-like objects, for zip etc. support.
    _path = attr.ib(type=str)

    def __attrs_post_init__(self):
        try:
            os.mkdir(self._path)
        except FileExistsError:
            pass

    @property
    def path(self):
        return self._path

    # layers

    def deleteGlyphSet(self, layerName):
        dir_ = self._contents[layerName]
        path = os.path.join(self._path, dir_)
        shutil.rmtree(path)
        del self._contents[layerName]

    def getGlyphSet(self, layerName):
        if layerName in self._contents:
            dir_ = self._contents[layerName]
        else:
            # TODO: cache this
            existing = set(d.lower() for d in self._contents.values())
            dir_ = self._contents[layerName] = userNameToFileName(
                layerName, existing=existing, prefix="glyphs.")
        path = os.path.join(self._path, dir_)
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        return GlyphSet(path)

    def writeLayerContents(self, layerOrder):
        """
        This must be called after all glyph sets have been written.
        """
        data = [(name, self._contents[name]) for name in layerOrder]
        path = os.path.join(self._path, LAYERCONTENTS_FILENAME)
        with open(path, "wb") as file:
            plistlib.dump(data, file)

    # bin

    def deleteData(self, fileName):
        path = os.path.join(self._path, DATA_DIRNAME, fileName)
        os.remove(path)

    def deleteImage(self, fileName):
        path = os.path.join(self._path, IMAGES_DIRNAME, fileName)
        os.remove(path)

    def writeData(self, fileName, data):
        path = os.path.join(self._path, DATA_DIRNAME, fileName)
        with open(path, "wb") as file:
            plistlib.dump(data, file)

    def writeImage(self, fileName, data):
        path = os.path.join(self._path, IMAGES_DIRNAME, fileName)
        with open(path, "wb") as file:
            plistlib.dump(data, file)

    # single writes

    def writeFeatures(self, text):
        path = os.path.join(self._path, FEATURES_FILENAME)
        if text:
            with open(path, "w") as file:
                file.write(text)
        else:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def writeGroups(self, data):
        path = os.path.join(self._path, GROUPS_FILENAME)
        if data:
            with open(path, "wb") as file:
                plistlib.dump(data, file)
        else:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def writeInfo(self, data):
        path = os.path.join(self._path, FONTINFO_FILENAME)
        if data:
            with open(path, "wb") as file:
                plistlib.dump(data, file)
        else:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def writeKerning(self, data):
        path = os.path.join(self._path, KERNING_FILENAME)
        if data:
            with open(path, "wb") as file:
                plistlib.dump(data, file)
        else:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def writeLib(self, data):
        path = os.path.join(self._path, LIB_FILENAME)
        if data:
            with open(path, "wb") as file:
                plistlib.dump(data, file)
        else:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass
