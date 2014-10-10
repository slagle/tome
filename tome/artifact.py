class ArtifactMeta(type):

    def __new__(meta, name, bases, dict):
        meta.validate_types(bases, dict)
        return type.__new__(meta, name, bases, dict)

    @staticmethod
    def validate_types(bases, dict):
        pass

class Artifact(object):

    __metaclass__ = ArtifactMeta

    def __init__(self, *args, **kwargs):
        kwargs = self._populate_kwargs(args, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.add()

    def _populate_kwargs(self, args, kwargs):
        slots = list(self.__slots__)
        arg_list = list(args)
        for arg in arg_list:
            kwargs[slots.pop(0)] = arg
        return kwargs

    def add(self, *args, **kwargs):
        raise NotImplementedError

    def remove(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def exists(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def collection(cls, objects):
        return ArtifactCollection(artifacts=objects)

class ArtifactCollection(object):

    def __init__(self, artifacts):
        self.artifacts = artifacts

    def realize(self):
        for artifact in self.artifacts:
            artifact.realize()

    def unrealize(self):
        for artifact in self.artifacts:
            artifact.unrealize()

    def is_realized(self):
        results = {}
        for artifact in self.artifacts:
            results.push(artifact, artifact.is_realized())

        return False not in results.values()

class ArtifactGroup(object):
    pass
