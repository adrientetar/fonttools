import attr
from ._common import Number
from fontTools.ufoLib.reader import UFOReader


@attr.s(slots=True)
class DataStore(object):
    getter = None

    _path = attr.ib(type=str)
    _fileNames = attr.ib(default=None, repr=False, type=list)
    _data = attr.ib(default=attr.Factory(dict), init=False, type=dict)
    _keys = attr.ib(init=False, repr=False, type=set)
    _scheduledForDeletion = attr.ib(default=attr.Factory(set), init=False, repr=False, type=set)

    def __attrs_post_init__(self):
        # TODO: this could be done lazily
        if self._fileNames is not None:
            keys = set(self._fileNames)
        else:
            keys = set()
        self._keys = keys

    def __contains__(self, fileName):
        return fileName in self._keys

    def __getitem__(self, fileName):
        data = self._data[fileName]
        if data is None:
            reader = UFOReader(self._path)
            data = self._data[fileName] = self.getter(reader, fileName)
        return data

    def __setitem__(self, fileName, data):
        # should we forbid overwrite?
        self._data[fileName] = data
        self._keys.add(fileName)
        if fileName in self._scheduledForDeletion:
            self._scheduledForDeletion.remove(fileName)

    def __delitem__(self, fileName):
        del self._data[fileName]
        self._keys.remove(fileName)
        self._scheduledForDeletion.add(fileName)


@attr.s(slots=True)
class Transformation(object):
    xScale = attr.ib(default=1, type=Number)
    xyScale = attr.ib(default=0, type=Number)
    yxScale = attr.ib(default=0, type=Number)
    yScale = attr.ib(default=1, type=Number)
    xOffset = attr.ib(default=0, type=Number)
    yOffset = attr.ib(default=0, type=Number)

    # getitem, len?
    # algebra ops?
    # translate, shear, skew, etc.?
    #
    # iter lets us create a tuple
    #
    # Qt QTransform methods should be a good reference
    # e.g. inverted() makes a copy, like reversed() for py iterators

    def __iter__(self):
        yield self.xScale
        yield self.xyScale
        yield self.yxScale
        yield self.yScale
        yield self.xOffset
        yield self.yOffset

    # translate?
    def move(self, dx, dy):
        self.xOffset += dx
        self.yOffset += dy
