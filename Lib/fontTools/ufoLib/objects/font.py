import attr
from ._common import OptString
from fontTools.ufoLib.reader import UFOReader
#from fontTools.ufoLib.objects.dataSet import DataSet
from fontTools.ufoLib.objects.guideline import Guideline
#from fontTools.ufoLib.objects.imageSet import ImageSet
from fontTools.ufoLib.objects.info import Info
from fontTools.ufoLib.objects.layerSet import LayerSet

DEFAULT_LAYER_NAME = "public.default"


@attr.s(slots=True)
class Font(object):
    _path = attr.ib(default=None, type=OptString)

    _features = attr.ib(default=None, init=False, repr=False, type=OptString)
    _groups = attr.ib(default=None, init=False, repr=False, type=dict)
    _guidelines = attr.ib(default=None, init=False, repr=False, type=list)
    _info = attr.ib(default=None, init=False, repr=False, type=Info)
    _kerning = attr.ib(default=None, init=False, repr=False, type=dict)
    _layers = attr.ib(default=attr.Factory(LayerSet), init=False, repr=False, type=LayerSet)

    #_data = attr.ib(init=False, repr=False, type=DataSet)
    #_images = attr.ib(init=False, repr=False, type=ImageSet)

    def __attrs_post_init__(self):
        # create data set
        # create image set
        if self._path is not None:
            reader = UFOReader(self._path)
            # load the layers
            for name, dirName in reader.getLayerContents():
                glyphSet = reader.getGlyphSet(dirName)
                self._layers.newLayer(name, glyphSet=glyphSet)
            # load data directory list
            # data = reader.getDataDirectoryListing()
            # self._data = DataSet(fileNames=data)
            # load images list
            # images = reader.getImageDirectoryListing()
            # self._images = ImageSet(fileNames=images)

        if not self._layers:
            self._layers.newLayer(DEFAULT_LAYER_NAME)

    def __contains__(self, name):
        return name in self._layers.defaultLayer

    def __delitem__(self, name):
        del self._layers.defaultLayer[name]

    def __getitem__(self, name):
        return self._layers.defaultLayer[name]

    def __iter__(self):
        return iter(self._layers.defaultLayer)

    def __len__(self):
        return len(self._layers.defaultLayer)

    def get(self, name, default=None):
        return self._layers.defaultLayer.get(name, default)

    def keys(self):
        return self._layers.defaultLayer.keys()

    @property
    def features(self):
        if self._features is None:
            if self._path is not None:
                reader = UFOReader(self._path)
                self._features = reader.readFeatures()
            else:
                self._features = ""
        return self._features

    @features.setter
    def features(self, text):
        self._features = text

    @property
    def guidelines(self):
        if self._guidelines is None:
            self.info
        return self._guidelines

    @property
    def groups(self):
        if self._groups is None:
            if self._path is not None:
                reader = UFOReader(self._path)
                self._groups = reader.readGroups()
            else:
                self._groups = {}
        return self._groups

    @property
    def info(self):
        if self._info is None:
            if self._path is not None:
                reader = UFOReader(self._path)
                data = reader.readInfo()
                # TODO: the guidelines should probably be made in the
                # reader for validation etc.
                # split into readInfo() and readGuidelines()
                #
                # idea: readGuidelines(self) which calls
                # appendGuideline() with a dict
                guidelines = data.pop("guidelines", [])
                self._info = Info(**data)
                for i in range(len(guidelines)):
                    data = guidelines[i]
                    for key in ("x", "y", "angle"):
                        if key not in data:
                            data[key] = 0
                    guidelines[i] = Guideline(**data)
                self._guidelines = guidelines
            else:
                self._info = Info()
                self._guidelines = []
        return self._info

    @property
    def kerning(self):
        if self._kerning is None:
            if self._path is not None:
                reader = UFOReader(self._path)
                self._kerning = reader.readKerning()
            else:
                self._kerning = {}
        return self._kerning

    @property
    def layers(self):
        return self._layers

    @property
    def lib(self):
        if self._lib is None:
            if self._path is not None:
                reader = UFOReader(self._path)
                self._lib = reader.readLib()
            else:
                self._lib = {}
        return self._lib

    @property
    def path(self):
        return self._path

    def addGlyph(self, glyph):
        self._layers.defaultLayer.addGlyph(glyph)

    def newGlyph(self, name):
        return self._layers.defaultLayer.newGlyph(name)

    def newLayer(self, name):
        return self._layers.newLayer(name)

    def renameGlyph(self, name, newName, overwrite=False):
        self._layers.defaultLayer.renameGlyph(name, newName, overwrite)

    def renameLayer(self, name, newName, overwrite=False):
        self._layers.renameLayer(name, newName, overwrite)

    def save(self, path=None):
        raise NotImplementedError
