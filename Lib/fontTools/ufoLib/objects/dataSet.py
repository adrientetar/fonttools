from fontTools.ufoLib.objects.misc import DataStore
from fontTools.ufoLib.reader import UFOReader


class DataSet(DataStore):
    getter = UFOReader.readData
