from fontTools.ufoLib.objects.misc import DataStore
from fontTools.ufoLib.reader import UFOReader


class ImageSet(DataStore):
    getter = UFOReader.readImage
