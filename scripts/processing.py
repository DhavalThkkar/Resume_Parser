# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 16:24:45 2021

@author: Dhaval
"""

import pandas as pd
import pytesseract
import os
import glob

from pyresparser import ResumeParser
from pyresparser.utils import extract_text

from PIL import Image
from pdf2image import convert_from_path

# System path variables
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path=r'C:\Users\MSI\Downloads\Release-21.03.0\poppler-21.03.0\Library\bin'

class document_processing:
    
    def __init__(self, resume, skills):
        
        self.resume = resume
        self.skills = skills
        
    def extract_resume(self):
        
        filepath = self.resume
        
        extension = filepath.split('.')[-1]
        extension = '.'+extension
        
        resume_ner_back = ResumeParser(filepath, file_path_txt="out_text.txt").get_extracted_data()
        resume_ner_main = ResumeParser(filepath).get_extracted_data()
        resume_txt = extract_text(filepath, extension=extension)
        
        return resume_ner_back, resume_ner_main, resume_txt
        
    def ocr_text(self):
        
        filepath = self.filepath
    
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)
        
        # Store all the pages of the PDF in a variable
        pages = convert_from_path(filepath, 500, poppler_path = poppler_path)
          
        # Counter to store images of each page of PDF to image
        image_counter = 1
          
        # Iterate through all the pages stored above
        for page in pages:
          
            # PDF page n -> page_n.jpg
            filename = "page_"+str(image_counter)+".jpg"
              
            # Save the image of the page in system
            page.save('temp/'+filename, 'JPEG')
          
            # Increment the counter to update filename
            image_counter = image_counter + 1
            
        ########## OCR ##########
        # Variable to get count of total number of pages
        filelimit = image_counter-1
        
        text_op = ''
        count = 0
        # Iterate from 1 to total number of pages
        for i in range(1, filelimit + 1):
            
            filename = "temp/page_"+str(i)+".jpg"
                  
            # Recognize the text as string in image using pytesserct
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
          
            text = text.replace('-\n', '')    
          
            # Finally, write the processed text to the file.
            text_op+=text
        
            count+=1
        
        with open('out_text.txt', 'w') as f:
            f.write(text_op)
        
        return text_op, count
    