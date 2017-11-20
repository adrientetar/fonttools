import attr
from fontTools.ufoLib.objects.glyph import Glyph, GlyphClasses
from fontTools.ufoLib.reader import GlyphSet

# TODO: layer.color, layer.lib?
# TODO: we could question the Layer/GlyphSet duality but I'd say it makes
# sense, fwiw. how do we guarantee that the UFO hasn't been written to though?


@attr.s(slots=True)
class Layer(object):
    _name = attr.ib(type=str)
    _glyphSet = attr.ib(default=None, repr=False, type=GlyphSet)
    _glyphs = attr.ib(init=False, repr=False, type=dict)
    _keys = attr.ib(init=False, repr=False, type=set)

    def __attrs_post_init__(self):
        self._glyphs = {}
        if self._glyphSet is not None:
            keys = set(self._glyphSet.keys())
        else:
            keys = set()
        self._keys = keys

    def __contains__(self, name):
        return name in self._keys

    def __delitem__(self, name):
        if name not in self._keys:
            raise KeyError("%s not in layer" % name)
        # XXX: we need to handle the case where the glyph isn't loaded
        # (or is on disk and we gotta purge it)
        del self._glyphs[name]
        self._keys.remove(name)

    def __getitem__(self, name):
        if name not in self._glyphs:
            self.loadGlyph(name)
        return self._glyphs[name]

    def __iter__(self):
        for name in self._keys:
            yield self[name]

    def __len__(self):
        return len(self._keys)

    def keys(self):
        # TODO: should we return a copy here?
        return self._keys

    @property  # rename from the parent? (which maintains a dict)
    def name(self):
        return self._name

    def addGlyph(self, glyph):
        if glyph.name in self._glyphs:
            raise KeyError("a glyph named \"%s\" already exists." % glyph.name)
        self._glyphs[glyph.name] = glyph
        self._keys.add(glyph.name)

    def loadGlyph(self, name):
        glyph = self._glyphSet.readGlyph(name, GlyphClasses)
        self._glyphs[name] = glyph

    def newGlyph(self, name):
        if name in self._glyphs:
            raise KeyError("a glyph named \"%s\" already exists." % name)
        self._glyphs[name] = glyph = Glyph(name)
        self._keys.add(name)
        return glyph
