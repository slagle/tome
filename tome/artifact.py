class ArtifactMeta(type):

    def __new__(meta, name, bases, classdict):
        meta.validate_types(bases, classdict)
        if 'remove' in classdict:
            classdict['remove'] = classmethod(classdict['remove'])
        if 'add' in classdict:
            classdict['add'] = classmethod(classdict['add'])
        if 'exists' in classdict:
            classdict['exists'] = classmethod(classdict['exists'])

        return type.__new__(meta, name, bases, classdict)

    @staticmethod
    def validate_types(bases, classdict):
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

    def exists(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def collection(cls, objects):
        return ArtifactCollection(artifacts=objects)

    def pre_add(self, *args, **kwargs):
        raise NotImplementedError

    def post_add(self, *args, **kwargs):
        raise NotImplementedError

    def pre_remove(self, *args, **kwargs):
        raise NotImplementedError

    def post_remove(self, *args, **kwargs):
        raise NotImplementedError

    def freeze(self, *args, **kwargs):
        raise NotImplementedError

    def unfreeze(self, *args, **kwargs):
        raise NotImplementedError

class ArtifactGroup(object):

    def __init__(self, artifacts=None):
        self.artifacts = artifacts or []

    def add(self):
        for artifact in self.artifacts:
            artifact.add()

    def remove(self):
        for artifact in self.artifacts:
            artifact.unrealize()

    def exists(self):
        results = {}
        for artifact in self.artifacts:
            results.push(artifact, artifact.exists())

        return False not in results.values()

