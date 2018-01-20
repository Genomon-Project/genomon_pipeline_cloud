#! /usr/bin/env python

import abc, subprocess

class Abstract_factory(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def execute(self, task, general_param):
        pass

    @abc.abstractmethod
    def print_command(self, task, general_param):
        pass

    @abc.abstractmethod
    def generate_commands(self, task, general_param):
        pass


class Dsub_factory(Abstract_factory):

    def execute(self, task, general_param):
        subprocess.call(self.generate_commands(task, general_param))

    def print_command(self, task, general_param):
        print ' '.join(self.generate_commands(task, general_param))

    def generate_commands(self, task, general_param):

        commands = ["dsub"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--logging", task.log_dir, "--script", task.script_file, \
                      "--image", task.image, "--tasks", task.task_file, "--wait"]
        return commands


class Awsub_factory(Abstract_factory):

    def execute(self, task, general_param):
        subprocess.call(self.generate_commands(task, general_param))

    def print_command(self, task, general_param):
        print ' '.join(self.generate_commands(task, general_param))

    def generate_commands(self, task, general_param):

        commands = ["awsub"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--script", task.script_file, "--image", task.image, "--tasks", task.task_file]

        return commands


class Batch_engine(object):

    def __init__(self, factory):
        self.execute = factory.execute
        self.print_command = factory.print_command


