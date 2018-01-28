#! /usr/bin/env python

import os

class Sample_conf(object):

    def __init__(self):

        self.fastq = {}
        self.bam_tofastq = {}
        self.bam_import = {}
        self.mutation_call = []
        self.sv_detection = []
        self.qc = []
        self.control_panel = {}
        self.fusion = []
        self.expression = []
        self.intron_retention = []
        # 
        # should add the file exist check here ?
        #
    

    def parse_file(self, file_path):

        file_ext = os.path.splitext(file_path)[1]

        file_data = []
        if file_ext.lower() == '.csv':
            file_data = self.parse_csv(file_path)
        elif file_ext.lower() == '.txt' or file_ext.lower() == '.tsv':
            file_data = self.parse_tsv(file_path)
        # elif file_ext.lower() == '.xlsx':
            # file_data = self.parse_xlsx(file_path)
        else:
            # 
            # should treat other cases ??
            #
            raise NotImplementedError("currently, we can just accept tsv and csv formats")
 

        file_data_trimmed = []
        for line_data in file_data:
       
            # skip empty lines
            if len(line_data) == 0: continue
 
            # line starting with '#' is comment
            if line_data[0].startswith('#'): continue
             
            # remove spaces
            line_data = map(lambda x: x.strip(' '), line_data)

            # skip if all the elements are empty
            if len(line_data) == line_data.count(''): continue

            file_data_trimmed.append(line_data)


        self.parse_data(file_data_trimmed)


    def parse_csv(self, file_path):

        _file_data = []
        import csv
        with open(file_path, 'r') as hIN:
            csv_obj = csv.reader(hIN)
            for cells in csv_obj:
                tempdata = []
                row_len = 0
                for cell in cells:
                    row_len += len(cell)
                    if (len(cell) == 0) and (row_len > 0):
                        continue
                    tempdata.append(cell)
                
                if row_len > 0:
                    _file_data.append(tempdata)

        return _file_data


    def parse_tsv(self, file_path):

        _file_data = []
        with open(file_path, 'r') as hIN:
            for line in hIN:
                F = line.rstrip().split('\t')
                tempdata = []
                row_len = 0
                for cell in F:
                    row_len += len(cell)
                    if (len(cell) == 0) and (row_len > 0):
                        continue
                    tempdata.append(cell)
                
                if row_len > 0:
                    _file_data.append(tempdata)

        return _file_data


    def parse_data(self, _data ):
    
        mode = ''
       
        sampleID_list = []
        mut_tumor_sampleID_list = []
        sv_tumor_sampleID_list = []
        qc_sampleID_list = []
        ff_sampleID_list = []
        exp_sampleID_list = []
        ir_sampleID_list = []
        
        for row in _data:
            if row[0].startswith('['):

                # header
                if row[0].lower() == '[fastq]':
                    mode = 'fastq'
                    continue
                elif row[0].lower() == '[bam_tofastq]':
                    mode = 'bam_tofastq'
                    continue
                elif row[0].lower() == '[bam_import]':
                    mode = 'bam_import'
                    continue
                elif row[0].lower() == '[mutation_call]':
                    mode = 'mutation_call'
                    continue
                elif row[0].lower() == '[sv_detection]':
                    mode = 'sv_detection'
                    continue
                elif row[0].lower() == '[qc]':
                    mode = 'qc'
                    continue
                elif row[0].lower() == '[summary]':
                    mode = 'qc'
                    continue
                elif row[0].lower() == '[controlpanel]':
                    mode = 'controlpanel'
                    continue
                elif row[0].lower() == '[fusion]':
                    mode = 'fusion'
                    continue
                elif row[0].lower() == '[expression]':
                    mode = 'expression'
                    continue
                elif row[0].lower() == '[intron_retention]':
                    mode = 'intron_retention'
                    continue
                else:
                    err_msg = "Section name should be either of [fastq], [bam_tofastq], [bam_import], " + \
                              "[mutation_call], [sv_detection], [controlpanel], [fusion], [expression] or [intron_retention]. " + \
                              "Also, sample name should not start with '['."
                    raise ValueError(err_msg)
            
            
            # section data
            if mode == 'fastq':

                sampleID = row[0]
                # 'None' is presereved for special string
                if sampleID == 'None':
                    err_msg = "None can not be used as sampleID"
                    raise ValueError(err_msg)

                if sampleID in sampleID_list:
                    err_msg = sampleID + " is duplicated."
                    raise ValueError(err_msg)

                sampleID_list.append(sampleID)

                if len(row) != 3:
                    err_msg = sampleID + ": the path for read1 (and read2) should be provided"
                    raise ValueError(err_msg)

                sequence1 = row[1].split(';')
                sequence2 = row[2].split(';')

                # file existence check in S3 and GCS should be implemented later
                """
                for s in range(len(sequence1)):
                    if not os.path.exists(sequence1[s]):
                        err_msg = sampleID + ": " + sequence1[s] +  " does not exists" 
                        raise ValueError(err_msg)
                    if not os.path.exists(sequence2[s]):
                        err_msg = sampleID + ": " + sequence2[s] +  " does not exists" 
                        raise ValueError(err_msg)
                    if sequence1[s] == sequence2[s]:
                        err_msg = sampleID + ": read1 and read2 are same path" 
                        raise ValueError(err_msg)
                """
                self.fastq[sampleID] = [sequence1, sequence2]

            elif mode == 'bam_tofastq':

                sampleID = row[0]
                # 'None' is presereved for special string
                if sampleID == 'None':
                    err_msg = "None can not be used as sampleID"
                    raise ValueError(err_msg)

                if sampleID in sampleID_list:
                    err_msg = sampleID + " is duplicated."
                    raise ValueError(err_msg)

                sampleID_list.append(sampleID)

                if len(row) != 2:
                    err_msg = sampleID + ": only one bam file is allowed"
                    raise ValueError(err_msg)

                sequences = row[1]
                
                # file existence check for S3 and GSC should be implemented later
                """
                for seq in sequences.split(";"):
                    if not os.path.exists(seq):
                        err_msg = sampleID + ": " + seq +  " does not exists"
                        raise ValueError(err_msg)
                """
                self.bam_tofastq[sampleID] = sequences
                
            elif mode == 'bam_import':

                sampleID = row[0]
                # 'None' is presereved for special string
                if sampleID == 'None':
                    err_msg = "None can not be used as sampleID"
                    raise ValueError(err_msg)

                if sampleID in sampleID_list:
                    err_msg = sampleID + " is duplicated."
                    raise ValueError(err_msg)

                sampleID_list.append(sampleID)

                if len(row) != 2:
                    err_msg = sampleID + ": only one bam file is allowed"
                    raise ValueError(err_msg)

                sequence = row[1]

                # file existence check should be implemented later
                """
                if not os.path.exists(sequence):
                    err_msg = sampleID + ": " + sequence +  " does not exists"
                    raise ValueError(err_msg)
                
                sequence_prefix, ext = os.path.splitext(sequence)
                if (not os.path.exists(sequence + '.bai')) and (not os.path.exists(sequence_prefix + '.bai')):
                    err_msg = sampleID + ": " + sequence +  " index does not exists"
                    raise ValueError(err_msg)
                """

                self.bam_import[sampleID] = sequence


            elif mode == 'mutation_call':

                tumorID = row[0]
                if tumorID not in sampleID_list:
                    err_msg = "[mutation_call] section, " + tumorID + " is not defined"
                    raise ValueError(err_msg)

                if tumorID in mut_tumor_sampleID_list:
                    err_msg = "[mutation_call] section, " + tumorID + " is duplicated"
                    raise ValueError(err_msg)

                normalID = row[1] if len(row) >= 2 and row[1] not in ['', 'None'] else None
                controlpanelID = row[2] if len(row) >= 3 and row[2] not in ['', 'None'] else None

                if normalID is not None and normalID not in sampleID_list:
                    err_msg = "[mutation_call] section, " + normalID + " is not defined"
                    raise ValueError(err_msg)

                mut_tumor_sampleID_list.append(tumorID)

                self.mutation_call.append((tumorID, normalID, controlpanelID))


            elif mode == 'sv_detection':

                tumorID = row[0]
                if tumorID not in sampleID_list:
                    err_msg = "[sv_detection] section, " + tumorID + " is not defined"
                    raise ValueError(err_msg)

                if tumorID in sv_tumor_sampleID_list:
                    err_msg = "[sv_detection] section, " + tumorID + " is duplicated"
                    raise ValueError(err_msg)

                normalID = row[1] if len(row) >= 2 and row[1] not in ['', 'None'] else None
                controlpanelID = row[2] if len(row) >= 3 and row[2] not in ['', 'None'] else None

                if normalID is not None and normalID not in sampleID_list:
                    err_msg = "[sv_detection] section, " + normalID + " is not defined"
                    raise ValueError(err_msg)

                sv_tumor_sampleID_list.append(tumorID)

                self.sv_detection.append((tumorID, normalID, controlpanelID))


            elif mode == 'qc':

                sampleID = row[0]
                if sampleID not in sampleID_list:
                    err_msg = "[qc] section, " + sampleID + " is not defined"
                    raise ValueError(err_msg)

                if sampleID in qc_sampleID_list:
                    err_msg = "[qc] section, " + sampleID + " is duplicated"
                    raise ValueError(err_msg)

                qc_sampleID_list.append(sampleID)

                self.qc.append(sampleID)


            elif mode == 'controlpanel':

                if len(row) <= 1:
                    err_msg = "[controlpanel] section, list item is none for the row: " + ','.join(row)
                    raise ValueError(err_msg)

                controlpanelID = row[0]

                for sample in row[1:]:
                    if sample not in sampleID_list:
                        err_msg = "[controlpanel] section, " + sample + " is not defined in " + \
                                    "controlpanelID: " + controlpanelID
                        raise ValueError(err_msg)
 
                self.control_panel[controlpanelID] = row[1:]


            elif mode == 'fusion':

                sampleID = row[0]
                if sampleID not in sampleID_list:
                    err_msg = "[fusion] section, " + sampleID + " is not defined"
                    raise ValueError(err_msg)

                if sampleID in ff_sampleID_list:
                    err_msg = "[fusion] section, " + sampleID + " is duplicated"
                    raise ValueError(err_msg)

                controlpanelID = row[1] if len(row) >= 2 and row[1] not in ['', 'None'] else None

                ff_sampleID_list.append(sampleID)

                self.fusion.append((sampleID,controlpanelID))


            elif mode == 'expression':

                sampleID = row[0]
                if sampleID not in sampleID_list:
                    err_msg = "[expression] section, " + sampleID + " is not defined"
                    raise ValueError(err_msg)

                if sampleID in exp_sampleID_list:
                    err_msg = "[expression] section, " + sampleID + " is duplicated"
                    raise ValueError(err_msg)

                exp_sampleID_list.append(sampleID)

                self.expression.append(sampleID)


            elif mode == 'intron_retention':

                sampleID = row[0]
                if sampleID not in sampleID_list:
                    err_msg = "[intron_retention] section, " + sampleID + " is not defined"
                    raise ValueError(err_msg)

                if sampleID in ir_sampleID_list:
                    err_msg = "[intron_retention] section, " + sampleID + " is duplicated"
                    raise ValueError(err_msg)

                ir_sampleID_list.append(sampleID)

                self.intron_retention.append(sampleID)

        # check whether controlpanleID in compare section is defined
        # for comp in self.compare:
        #     if comp[2] is not None and comp[2] not in self.controlpanel:
        #         err_msg = "[compare] section, controlpanelID: " + comp[2] + " is not defined"
        #         raiseValueError(err_msg)



# global sample_conf 
# sample_conf = Sample_conf()


