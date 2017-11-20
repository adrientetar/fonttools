import attr


@attr.s(slots=True)
class Component(object):
    # TODO: validator should verify that glyph exists
    baseGlyph = attr.ib(type=str)
    # TODO: need a more sophisticated validator here
    # len(6), Number
    transformation = attr.ib(type=tuple)
    identifier = attr.ib(default=None, type=str)
