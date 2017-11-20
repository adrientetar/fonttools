import attr
from fontTools.ufoLib.objects.glyph import Glyph
from fontTools.ufoLib.reader import GlyphSet

# TODO: layer.color, layer.lib?
# TODO: we could question the Layer/GlyphSet but I think it makes sense,
# fwiw. how do we guarantee that the UFO hasn't been written to though?


@attr.s(slots=True)
class Layer(object):
    _name = attr.ib(type=str)
    _glyphSet = attr.ib(default=None, repr=False, type=GlyphSet)
    _glyphs = attr.ib(init=False, repr=False, type=list)

    def __attrs_post_init__(self):
        self._glyphs = {}

    def __getitem__(self, name):
        if name not in self._glyphs:
            self.loadGlyph(name)
        return self._glyphs[name]

    def __iter__(self):
        for name in self._glyphSet.keys():
            yield self[name]

    @property  # rename from the parent? (which maintains a dict)
    def name(self):
        return self._name

    def loadGlyph(self, name):
        glyph = self._glyphSet.readGlyph(name)
        self._glyphs[name] = glyph

    # TODO: this should probably be re-exported in the Font
    def newGlyph(self, name):
        if name in self._glyphs:
            raise KeyError("a glyph named \"%s\" already exists." % name)
        self._glyphs[name] = glyph = Glyph(name)
        return glyph
