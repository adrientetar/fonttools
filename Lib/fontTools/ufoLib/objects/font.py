import attr
from ._common import String
from fontTools.ufoLib.reader import UFOReader
from fontTools.ufoLib.objects.features import Features
from fontTools.ufoLib.objects.guideline import Guideline
from fontTools.ufoLib.objects.info import Info
from fontTools.ufoLib.objects.layerSet import LayerSet

DEFAULT_LAYER_NAME = "public.default"


@attr.s(slots=True)
class Font(object):
    _path = attr.ib(default=None, type=String)
    _features = attr.ib(init=False, repr=False, type=Features)
    _guidelines = attr.ib(init=False, repr=False, type=list)
    _info = attr.ib(init=False, repr=False, type=Info)
    _layers = attr.ib(init=False, repr=False, type=LayerSet)

    def __attrs_post_init__(self):
        self._features = None
        self._guidelines = None
        self._info = None
        self._layers = LayerSet()
        # create image set
        # create data set
        if self._path is not None:
            reader = UFOReader(self._path)
            # load the layers
            for name, dirName in reader.getLayerContents():
                glyphSet = reader.getGlyphSet(dirName)
                self._layers.newLayer(name, glyphSet=glyphSet)
            # load images list
            # ..
            # load data directory list
            # ..

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
                text = reader.readFeatures()
            else:
                text = ""
            self._features = Features(text)
        return self._features

    @property
    def guidelines(self):
        if self._guidelines is None:
            self.info
        return self._guidelines

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
    def layers(self):
        return self._layers

    @property
    def path(self):
        return self._path

    def addGlyph(self, glyph):
        self._layers.defaultLayer.addGlyph(glyph)

    def newGlyph(self, name):
        return self._layers.defaultLayer.newGlyph(name)

    def newLayer(self, name):
        return self._layers.newLayer(name)

    def save(self, path=None):
        raise NotImplementedError
