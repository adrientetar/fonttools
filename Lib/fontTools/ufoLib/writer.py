import attr
from fontTools.ufoLib.constants import (
    DATA_DIRNAME, FEATURES_FILENAME, FONTINFO_FILENAME, GROUPS_FILENAME,
    KERNING_FILENAME, IMAGES_DIRNAME, LIB_FILENAME)
import os
import plistlib


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
        raise NotImplementedError  # XXX

    def getGlyphSet(self, layerName):
        raise NotImplementedError

    def writeLayerContents(self, layerOrder):
        raise NotImplementedError

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
