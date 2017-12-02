import attr
from collections import OrderedDict
from fontTools.ufoLib.objects.layer import Layer


@attr.s(slots=True)
class LayerSet(object):
    _layers = attr.ib(init=False, type=OrderedDict)

    def __attrs_post_init__(self):
        self._layers = OrderedDict()

    def __contains__(self, name):
        return name in self._layers

    def __delitem__(self, name):
        del self._layers[name]

    def __getitem__(self, name):
        return self._layers[name]

    def __iter__(self):
        return iter(self._layers.values())

    def __len__(self):
        return len(self._layers)

    @property
    def defaultLayer(self):
        try:
            return next(iter(self))
        except StopIteration:
            pass
        return None

    @defaultLayer.setter
    def defaultLayer(self, layer):
        hasLayer = False
        layers = OrderedDict()
        layers[layer.name] = layer
        for layer_ in self:
            if layer_ == layer:
                hasLayer = True
                continue
            layers[layer_.name] = layer_
        if not hasLayer:
            raise KeyError("layer \"%s\" is not in the layer set." % layer)
        self._layers = layers

    @property
    def layerOrder(self):
        return list(self._layers)

    @layerOrder.setter
    def layerOrder(self, order):
        assert set(order) == set(self._layers)
        layers = OrderedDict()
        for name in order:
            layers[name] = self._layers[name]
        self._layers = layers

    def newLayer(self, name, glyphSet=None):
        if name in self._layers:
            raise KeyError("a layer named \"%s\" already exists." % name)
        self._layers[name] = layer = Layer(name, glyphSet)
        # TODO: should this be done in Layer ctor?
        if glyphSet is not None:
            glyphSet.readLayerInfo(layer)
        return layer

    def renameGlyph(self, name, newName, overwrite=False):
        # Note: this would be easier if the glyph contained the layers!
        if name == newName:
            return
        # make sure we're copying something
        if not any(name in layer for layer in self):
            raise KeyError("no glyph named \"%s\" exists." % name)
        # prepare destination, delete if overwrite=True or error
        for layer in self:
            if newName in self._layers:
                if overwrite:
                    del layer[newName]
                else:
                    raise KeyError("a glyph named \"%s\" already exists." % newName)
        # now do the move
        for layer in self:
            if name in layer:
                layer[newName] = glyph = layer.pop(name)
                glyph._name = newName

    def renameLayer(self, name, newName, overwrite=False):
        if name == newName:
            return
        if not overwrite and newName in self._layers:
            raise KeyError("a layer named \"%s\" already exists." % newName)
        self._layers[newName] = layer = self._layers.pop(name)
        layer._name = newName
