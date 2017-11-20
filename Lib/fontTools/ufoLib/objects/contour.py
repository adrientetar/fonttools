
# TODO: drawPoints?

# TODO: will need a segment validator here


class Contour(list):

    def __repr__(self):
        base = super().__repr__()
        return "Contour(%s)" % base
