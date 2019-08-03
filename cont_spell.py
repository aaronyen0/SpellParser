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
        self.template_id
        self.log_id_lt = log_id_lt
        


