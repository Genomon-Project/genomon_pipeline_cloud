#! /usr/bin/env python

import abc, subprocess

class Abstract_factory(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, task):
        pass

    @abc.abstractmethod
    def print_job(self, task):
        pass


class Dsub_factory(Abstract_factory):

    def execute(self, task):
        subprocess.call(["dsub"] + task.resource_param.split(' ') + \
                        ["--logging", task.log_dir, "--script", task.script_file, \
                         "--image", task.image, "--tasks", task.task_file, "--wait"])

    def print_job(self, task):
        print ' '.join(["dsub",
                         task.resource_param,
                         "--logging " + task.log_dir,
                         "--script " + task.script_file,
                         "--image " + task.image,
                         "--tasks "+ task.task_file,
                         "--wait"])



class Batch_engine(object):

    def __init__(self, factory):
        self.execute = factory.execute
        self.print_job = factory.print_job
 

 
