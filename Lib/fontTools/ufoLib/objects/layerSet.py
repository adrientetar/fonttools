import attr
from collections import OrderedDict
from fontTools.ufoLib.objects.layer import Layer


@attr.s()
class LayerSet(object):
    _layers = attr.ib(init=False, type=OrderedDict)

    def __attrs_post_init__(self):
        self._layers = OrderedDict()
        self.__contains__ = self._layers.__contains__
        self.__delitem__ = self._layers.__delitem__
        self.__getitem__ = self._layers.__getitem__
        self.__len__ = self._layers.__len__

    # TODO: clear, layers getter?

    def __iter__(self):
        return iter(self._layers.values())

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
