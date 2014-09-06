
class Artifact(object):

    def __init__(self, *args, **kwargs):
        kwargs = self._populate_kwargs(args, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def realize(cls, *args, **kwargs):
        inst = cls._inst_from_kwargs(args, kwargs)
        return inst._realize()

    @classmethod
    def unrealize(cls, *args, **kwargs):
        inst = cls._inst_from_kwargs(args, kwargs)
        return inst._unrealize()

    @classmethod
    def is_realized(cls, *args, **kwargs):
        inst = cls._inst_from_kwargs(args, kwargs)
        return inst._is_realized()

    @classmethod
    def _populate_kwargs(cls, args, kwargs):
        slots = list(cls.__slots__)
        arg_list = list(args)
        for arg in arg_list:
            kwargs[slots.pop(0)] = arg
        return kwargs

    @classmethod
    def _inst_from_kwargs(cls, args, kwargs):
        kwargs = cls._populate_kwargs(args, kwargs)
        return cls(**kwargs)
