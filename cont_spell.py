import sys
import re
import os
import numpy as np
import pandas as pd
import obj_pickle_save_load

class LCSObject:
    """ Class object to store some information of a template:
    """
    def __init__(self, log_template: str, template_id: int, log_id_lt: list):
        """
        Initialize the template object:
            1. log_template(str): the template
            2. template_id(int): the ID of this template
            3. log_id_lt(list): a group with the same template
        """
        self.log_template = log_template
        self.template_id = template_id
        self.log_id_lt = log_id_lt
        


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