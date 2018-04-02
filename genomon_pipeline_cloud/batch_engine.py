#! /usr/bin/env python

import abc, subprocess

class Abstract_factory(object):
    __metaclass__ = abc.ABCMeta
    dryrun = False
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def execute_closure(self, task, general_param):
        pass

    @abc.abstractmethod
    def print_command_closure(self, task, general_param):
        pass

    @abc.abstractmethod
    def generate_commands(self, task, general_param):
        pass

    def base_commands(self, commands):
        if self.dryrun:
            return ["echo", ">>"] + commands
        return commands

class Dsub_factory(Abstract_factory):

    def execute_closure(self, general_param):
        def execute(task):
            subprocess.check_call(self.generate_commands(task, general_param))
        return execute

    def seq_execute_closure(self, general_param):
        def seq_execute(tasks):
            for task in tasks:
                subprocess.check_call(self.generate_commands(task, general_param))
        return seq_execute

    def print_command_closure(self, general_param):
        def print_command(task):
            print ' '.join(self.generate_commands(task, general_param))
        return print_command

    def generate_commands(self, task, general_param):

        commands = ["dsub"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--logging", task.log_dir, "--script", task.script_file, \
                      "--image", task.image, "--tasks", task.task_file, "--wait"]
        return self.base_commands(commands)


class Azmon_factory(Abstract_factory):

    def execute_closure(self, general_param):
        def execute(task):
            subprocess.check_call(self.generate_commands(task, general_param))
        return execute

    def seq_execute_closure(self, general_param):
        def seq_execute(tasks):
            for task in tasks:
                subprocess.check_call(self.generate_commands(task, general_param))
        return seq_execute
    
    def print_command_closure(self, general_param):
        def print_command(task):
            print ' '.join(self.generate_commands(task, general_param))
        return print_command

    def generate_commands(self, task, general_param):

        commands = ["azurebatchmon"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--script", task.script_file, "--image", task.image, "--tasks", task.task_file]

        return self.base_commands(commands)


class Awsub_factory(Abstract_factory):

    def execute_closure(self, general_param):
        def execute(task):
            subprocess.check_call(self.generate_commands(task, general_param))
        return execute

    def seq_execute_closure(self, general_param):
        def seq_execute(tasks):
            for task in tasks:
                subprocess.check_call(self.generate_commands(task, general_param))
        return seq_execute
    
    def print_command_closure(self, general_param):
        def print_command(task):
            print ' '.join(self.generate_commands(task, general_param))
        return print_command

    def generate_commands(self, task, general_param):

        commands = ["awsub"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--script", task.script_file, "--image", task.image, "--tasks", task.task_file]

        return self.base_commands(commands)

class Ecsub_factory(Abstract_factory):
    
    s3_wdir = ""
    wdir = "/tmp/ecsub"
    
    def execute_closure(self, general_param):
        def execute(task):
            subprocess.check_call(self.generate_commands(task, general_param))
        return execute

    def seq_execute_closure(self, general_param):
        def seq_execute(tasks):
            for task in tasks:
                subprocess.check_call(self.generate_commands(task, general_param))
        return seq_execute
    
    def print_command_closure(self, general_param):
        def print_command(task):
            print ' '.join(self.generate_commands(task, general_param))
        return print_command

    def generate_commands(self, task, general_param):

        commands = ["ecsub", "submit"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--script", task.script_file, "--image", task.image, "--tasks", task.task_file] + \
                     ["--aws-s3-bucket", self.s3_wdir, "--wdir", self.wdir]

        return self.base_commands(commands)
        
class Batch_engine(object):

    def __init__(self, factory, general_param):
        self.execute = factory.execute_closure(general_param)
        self.seq_execute = factory.seq_execute_closure(general_param)
        self.print_command = factory.print_command_closure(general_param)


