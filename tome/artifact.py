class ArtifactMeta(type):

    def __new__(meta, name, bases, classdict):
        meta.validate_types(bases, classdict)
        if 'remove' in classdict:
            classdict['_remove'] = classmethod(classdict['remove'])
        if 'add' in classdict:
            classdict['_add'] = classmethod(classdict['add'])
        if 'exists' in classdict:
            classdict['_exists'] = classmethod(classdict['exists'])

        classdict['do_commands'] = True

        return type.__new__(meta, name, bases, classdict)

    @staticmethod
    def validate_types(bases, classdict):
        pass

class Artifact(object):

    __metaclass__ = ArtifactMeta

    do_commands = False

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

    def pre_add(self, *args, **kwargs):
        raise NotImplementedError

    def post_add(self, *args, **kwargs):
        raise NotImplementedError

    def pre_remove(self, *args, **kwargs):
        raise NotImplementedError

    def pre_remove(self, *args, **kwargs):
        raise NotImplementedError

class ArtifactCollection(object):

    def __init__(self, artifacts):
        self.artifacts = artifacts

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

class ArtifactGroup(object):
    pass
