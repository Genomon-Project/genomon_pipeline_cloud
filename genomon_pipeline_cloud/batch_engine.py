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
            print (' '.join(self.generate_commands(task, general_param)))
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
            print (' '.join(self.generate_commands(task, general_param)))
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
            print (' '.join(self.generate_commands(task, general_param)))
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
            print (' '.join(self.generate_commands(task, general_param)))
        return print_command

    def generate_commands(self, task, general_param):

        commands = ["ecsub", "submit"] + general_param.split(' ') + task.resource_param.split(' ') + \
                     ["--script", task.script_file, "--image", task.image, "--tasks", task.task_file] + \
                     ["--aws-s3-bucket", self.s3_wdir, "--wdir", self.wdir]

        return self.base_commands(commands)
    
    def print_summary(self, run_conf, log_dir):
        import glob
        import json
        
        dirs = glob.glob("%s/*%s*" % (self.wdir, run_conf.analysis_timestamp))
        
        sim_cost = 0.0
        od_cost = 0.0
        jobs = []
        header = ""
        for d in sorted(dirs):
            files = glob.glob("%s/log/summary*.log" % (d))
            for f in sorted(files):
                summary = json.load(open(f))
                for j in summary["Jobs"]:
                    job = {
                        "ClusterName": summary["ClusterName"],
                        "Ec2instancetype": j["Ec2instancetype"],
                        "Ec2InstanceDiskSize": summary["Ec2InstanceDiskSize"],
                        "Spot": j["Spot"],
                        "WorkHours": j["WorkHours"]
                    }
                    job["OdPrice"] = j["OdPrice"]
                    if j["Spot"]:
                        job["SpotPrice"] = j["SpotPrice"]
                        job["WorkHours*Price"] = j["WorkHours"] * j["SpotPrice"]
                    else:
                        job["WorkHours*Price"] = j["WorkHours"] * j["OdPrice"]
                    
                    if len(header) == 0:
                        header = ",".join(sorted(job.keys()))
                        
                    jobs.append(job)
                    sim_cost += job["WorkHours*Price"]
                    od_cost += j["WorkHours"] * j["OdPrice"]
        
        log_file = "%s/summary-%s.csv" % (log_dir, run_conf.analysis_timestamp)
        print ("Total cost of this instance usage is %.3f USD. See detail, %s" % (sim_cost, log_file))
        
        t = "TotalInstanceCost,%.3f\n" % (sim_cost)
        t += "OndemandCost,%.3f\n" % (od_cost)
        t += "%s\n" % (header)
        for j in jobs:
            for k in sorted(j.keys()):
                t += "%s," % (j[k])
            t += "\n"
        open(log_file, "w").write(t)
        
class Batch_engine(object):

    def __init__(self, factory, general_param):
        self.execute = factory.execute_closure(general_param)
        self.seq_execute = factory.seq_execute_closure(general_param)
        self.print_command = factory.print_command_closure(general_param)


