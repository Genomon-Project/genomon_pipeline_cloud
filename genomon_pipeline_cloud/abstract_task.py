#! /usr/bin/env python

import abc

class Abstract_task(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, script_file, image, resoucer_param, log_dir):
        self.script_file = script_file
        self.image = image
        self.resource_param = resource_param
        self.log_dir = log_dir

    @abc.abstractmethod
    def task_file_generation():
        pass

