#! /usr/bin/env python

import abc

class Abstract_factory(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, task):
        pass


class Dsub_factory(Abstract_factory):

    def execute(self, task):
        subprocess.call(["dsub",
                         task.resource_param,
                         "--logging", task.log_dir,
                         "--script", task.script_file,
                         "--image", task.image,
                         "--tasks", task.task_file,
                         "--wait"]) 

class Batch_engine(object):

    def __init__(self, factory):
        self.execute = factory.execute
 

    factory = Dsub_factory()
    batch_engine = Batch_engine(factory)
    
 
