# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 13:55:12 2021

@author: MSI
"""

from pyresparser import ResumeParser
from pyresparser.utils import extract_text

from cleantext import clean

def extract_resume(filepath):
    
    extension = filepath.split('.')[-1]
    extension = '.'+extension
    
    resume_ner = ResumeParser(filepath, file_path_txt="out_text.txt").get_extracted_data()
    resume_txt = extract_text(filepath, extension=extension)
    
    return resume_ner, resume_txt

ner, str_r = extract_resume('sample/Dhaval_Thakkar_Resume.pdf')

