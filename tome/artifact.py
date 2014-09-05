
class ArtifactMeta(type):

    def __new__(mcs, name, bases, dict):
        return super(ArtifactMeta, mcs).__new__(mcs, name, bases, dict)


class Artifact(object):

    # __metaclass__ = ArtifactMeta

    def __new__(cls, *args, **kwargs):
        cls.__slots__ = cls.__dict__.keys()
        return super(Artifact, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        i = 0
        for arg in args:
            setattr(self, self.__slots__[i], arg)
            i += 1

        for k, v in kwargs:
            setattr(self, k, v)

    @classmethod
    def realize(cls, *args, **kwargs):
        if args or kwargs:
            return cls(*args, **kwargs)._realize()
        else:
            return cls()._realize()

    @classmethod
    def is_realized(cls, *args, **kwargs):
        if args or kwargs:
            return cls(*args, **kwargs)._is_realized()
        else:
            return cls()._is_realized()

    @classmethod
    def unrealize(cls, *args, **kwargs):
        if args or kwargs:
            return cls(*args, **kwargs)._unrealize()
        else:
            return cls()._unrealize()


