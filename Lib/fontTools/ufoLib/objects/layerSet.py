import attr
from collections import OrderedDict
from fontTools.ufoLib.objects.layer import Layer


@attr.s(slots=True)
class LayerSet(object):
    _layers = attr.ib(init=False, type=OrderedDict)

    def __attrs_post_init__(self):
        self._layers = OrderedDict()

    # TODO: clear, get(), layers getter?

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

    def layerNames(self):
        return iter(self._layers)

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
        return layer
