import sys
import re
import os
import numpy as np
import pandas as pd
import obj_pickle_save_load

class SpellTemplateClust:
    """ Class object to store information of a template:
    """
    def __init__(self, log_template: list, template_id: int, log_id_lt: list=[]):
        """
        Initialize the template object:

        Args:
            log_template(list): the template
            template_id(int): the ID of this template
            log_id_lt(list): a group with the same template
        """
        self.log_template = log_template
        self.template_id = template_id
        self.log_id_lt = log_id_lt
        

class SpellParserInfo:
    """
    inofrmation of a Spell-Parser
    """

    def __init__(self, tau: float, template_clust_lt: list=[]):
        self.tau = tau
        self.template_clust_lt = []

    def load_parser_info(self, file_name):
        sl_obj = obj_pickle_save_load.ObjPickleSaveLoad(file_name=file_name, obj_type=SpellParserInfo)
        loaded_obj = sl_obj.obj_load()
        if loaded_obj:
            self.tau = loaded_obj.tau
            self.template_clust_lt = loaded_obj.template_clust_lt
            return True
        return False

    def save_parser_info(self, file_name):
        new_parser_obj = SpellParserInfo(tau=self.tau)
        for clust in self.template_clust_lt:
            new_clust = SpellTemplateClust(log_template=clust.log_template, template_id=clust.template_id)
            new_parser_obj.template_clust_lt.append(new_clust)

        sl_obj = obj_pickle_save_load.ObjPickleSaveLoad(file_name=file_name, obj_type=SpellParserInfo)
        return sl_obj.obj_save(new_parser_obj)



class ContSpell:
    """ LogParser class

    Attributes
    ----------
        path : the path of the input file
        logName : the file name of the input file
        savePath : the path of the output file
        tau : how much percentage of tokens matched to merge a log message
    """

    def __init__(self, indir='./', outdir='./result/', log_format=None, tau=0.5, rex=[], keep_para=True):
        self.path = indir
        self.logName = None
        self.savePath = outdir
        self.tau = tau
        self.logformat = log_format
        self.df_log = None
        self.rex = rex
        self.keep_para = keep_para

    def longest_common_subsequence(self, seq1: list, seq2: list):
        """
        Given two sequences of string, return the longest common subsequence

        Args:
            seq1(list): a list contains some strings
            seq2(list): a list contains some strings

        Return:
            result(list): a list contains some strings, LCS of seq1 and seq2
        """
        len1 = len(seq1)
        len2 = len(seq2)

        dp = [[0 for j in range(len2 + 1)] for i in range(len1 + 1)]
        # row 0 and column 0 are initialized to 0 already
        for i in range(len1):
            for j in range(len2):
                if seq1[i] == seq2[j]:
                    dp[i + 1][j + 1] = dp[i][j] + 1
                else:
                    dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

        # read the substring out from the matrix
        result = []
        idx1 = len1
        idx2 = len2
        while idx1 != 0 and idx2 != 0:
            if dp[idx1][idx2] == dp[idx1 - 1][idx2]:
                idx1 -= 1
            elif dp[idx1][idx2] == dp[idx1][idx2 - 1]:
                idx2 -= 1
            else:
                assert seq1[idx1 - 1] == seq2[idx2 - 1]
                result.insert(0,seq1[idx1 - 1])
                idx1 -= 1
                idx2 -= 1
        return result


    def lcs_match(self, template_clust_lt: list, new_seq: list, tau: float):
        ret_clust = None

        max_len = -1
        max_clust = None
        set_seq = set(new_seq)
        new_seq_len = len(new_seq)
        for clust in template_clust_lt:
            set_template = set(clust.log_template)
            if len(set_seq & set_template) < tau * new_seq_len:
                continue

            lcs = self.longest_common_subsequence(new_seq, clust.log_template)
            if len(lcs) > max_len or (len(lcs) == max_len and len(clust.log_template) < len(max_clust.log_template)):
                max_len = len(lcs)
                max_clust = clust

        # LCS should be large then tau * len(itself)
        if float(max_len) >= tau * new_seq_len:
            ret_clust = max_clust

        return ret_clust   
