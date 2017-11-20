import attr
from ._common import Number, String


# Be more deterministic in the attrs: x y and angle are required
# https://github.com/unified-font-object/ufo-spec/issues/47#issuecomment-288461554

@attr.s(slots=True)
class Guideline(object):
    x = attr.ib(type=Number)
    y = attr.ib(type=Number)
    angle = attr.ib(type=Number)
    name = attr.ib(default=None, type=String)
    color = attr.ib(default=None, type=String)
    identifier = attr.ib(default=None, type=String)
