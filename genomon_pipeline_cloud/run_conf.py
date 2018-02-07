#! /usr/bin/env python

import os
import subprocess
import datetime

date_format = "{year:0>4d}-{month:0>2d}-{day:0>2d} {hour:0>2d}:{min:0>2d}:{second:0>2d}"
timestamp_format = "{year:0>4d}{month:0>2d}{day:0>2d}-{hour:0>2d}{min:0>2d}{second:0>2d}"

#global run_conf

class Run_conf(object):
    """
    class for job related parameters
    """

    def __init__(self, sample_conf_file = None, 
                        project_root = None, 
                        analysis_type = None,
                        genomon_conf_file = None):

        self.sample_conf_file = sample_conf_file
        self.sample_conf_name = os.path.splitext(os.path.basename(sample_conf_file))[0]
        self.project_root = project_root
        self.genomon_conf_file = genomon_conf_file 
        self.analysis_type = analysis_type 
        
        now = datetime.datetime.now()
        self.analysis_date = date_format.format(
                                 year = now.year,
                                 month = now.month,
                                 day = now.day,
                                 hour = now.hour,
                                 min = now.minute,
                                 second = now.second)

        self.analysis_timestamp = timestamp_format.format(
                                      year = now.year,
                                      month = now.month,
                                      day = now.day,
                                      hour = now.hour,
                                      min = now.minute,
                                      second = now.second)

        proc = subprocess.Popen(['genomon_pipeline_cloud --version 2>&1'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.pipeline_version = (proc.communicate()[0]).split("\n")[0]
        
    def get_meta_info(self, image):
        #import pwd
        #return "# Docker Image: %s\n# Analysis Date: %s\n# User: %s" % (
        #            image, 
        #            self.analysis_date, 
        #            pwd.getpwuid(os.getuid()).pw_name
        #        )
        return "# Docker Image: %s" % (
                    image
                )

    def get_owner_info(self):
        import pwd
        return pwd.getpwuid(os.getuid()).pw_name

#run_conf = Run_conf()

