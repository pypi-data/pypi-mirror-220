#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2019 Python Software Foundation
# Author: icewater.song
# Contact: icersong@gmail.com
from __future__ import print_function

__version__ = "0.1.0"

import os.path

import yaml
from yaml import Loader
from yaml import ScalarNode
from yaml import MappingNode
from yaml import SequenceNode
from yaml.constructor import ConstructorError


class IncudeLoader(Loader):
    """
    education:    !include education.yaml
    activities:   !include [schools.yaml, conferences.yaml, workshops.yaml]
    publications: !include {
                        peer_reviewed: publications/peer_reviewed.yaml,
                        internal: publications/internal.yaml}
    """

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super().__init__(stream)
        Loader.add_constructor("!include", self.__class__.include)
        Loader.add_constructor("!import", self.__class__.include)

    def include(self, node):
        if isinstance(node, ScalarNode):
            return self.extractFile(self.construct_scalar(node))

        elif isinstance(node, SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result += self.extractFile(filename)
            return result

        elif isinstance(node, MappingNode):
            result = {}
            for k, v in self.construct_mapping(node).items():
                result[k] = self.extractFile(v)
            return result

        else:
            print("Error:: unrecognised node type in !include statement")
            raise ConstructorError

    def extractFile(self, filename):
        filepath = os.path.join(self._root, filename)
        with open(filepath, "rb") as f:
            return yaml.load(f, self.__class__)
