import attr

# TODO: do we need a class? or make it a str?


@attr.s
class Features(object):
    text = attr.ib(default=attr.Factory(str), type=str)
