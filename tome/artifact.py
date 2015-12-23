#!/usr/bin/env python
#
# Copyright 2015 James Slagle <james.slagle@gmail.com>
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class ArtifactMeta(type):

    def __new__(meta, name, bases, classdict):
        meta.validate_types(bases, classdict)
        if 'delete' in classdict:
            classdict['delete'] = classmethod(classdict['delete'])
        if 'create' in classdict:
            classdict['create'] = classmethod(classdict['create'])
        if 'exists' in classdict:
            classdict['exists'] = classmethod(classdict['exists'])

        return type.__new__(meta, name, bases, classdict)

    @staticmethod
    def validate_types(bases, classdict):
        pass

class Artifact(object):
    """Artifact base class
    """

    __metaclass__ = ArtifactMeta

    def __init__(self, *args, **kwargs):
        kwargs = self._populate_kwargs(args, kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.create()

    def _populate_kwargs(self, args, kwargs):
        slots = list(self.__slots__)
        arg_list = list(args)
        for arg in arg_list:
            kwargs[slots.pop(0)] = arg
        return kwargs

    def __str__(self):
        return self.__name__

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def exists(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def group(cls, objects):
        return ArtifactGroup(artifacts=objects)

    def pre_create(self, *args, **kwargs):
        raise NotImplementedError

    def post_create(self, *args, **kwargs):
        raise NotImplementedError

    def pre_delete(self, *args, **kwargs):
        raise NotImplementedError

    def post_delete(self, *args, **kwargs):
        raise NotImplementedError

    def freeze(self, *args, **kwargs):
        raise NotImplementedError

    def unfreeze(self, *args, **kwargs):
        raise NotImplementedError

class ArtifactGroup(object):
    """Artifact Group base class
    """

    def __init__(self, artifacts=None):
        self.artifacts = artifacts or []

    def create(self):
        for artifact in self.artifacts:
            artifact.create()

    def delete(self):
        for artifact in self.artifacts:
            artifact.delete()

    def exists(self):
        results = {}
        for artifact in self.artifacts:
            results.push(artifact, artifact.exists())

        return False not in results.values()
