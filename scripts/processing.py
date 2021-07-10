# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 16:24:45 2021

@author: Dhaval
"""

import pandas as pd
import pytesseract
import os
import glob
import nltk

from pyresparser import ResumeParser
from pyresparser.utils import extract_text

from PIL import Image
from pdf2image import convert_from_path

# System path variables
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path=r'C:\Users\MSI\Downloads\Release-21.03.0\poppler-21.03.0\Library\bin'

class document_processing:
    
    def __init__(self, resume, skills):
        
        skills = pd.read_csv('skills.csv')
        
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
        
        filepath = self.resume
    
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
    
    def find_unigram(df, column):
        
        unigrams  = (df[column].str.lower()
                    .str.replace(r'[^a-z\s]', '')
                    .str.split(expand=True)
                    .stack()).reset_index(drop=True)
        
        unigrams = hero.clean(unigrams)
        un_df = pd.DataFrame(unigrams, columns = ['text'])
        
        return un_df
    
    def find_match(source, match):
        
        # Remove the null values 
        match.dropna(inplace=True)
        match.reset_index(drop=True)
        match.columns = ['text']
        match['text'] = hero.clean(match['text'])
        
        # Find the max val
        max_val = len(match)
        
        # Find the skills that match with the resume
        df = pd.merge(source, match, on = 'text')
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True)
        
        # Skills matching
        match_skills = len(df)
        
        if match_skills == 0:
            lst_skills = []
            score = 0
        elif match_skills > 0:
            lst_skills = df['text'].tolist()
            score = int((match_skills / max_val) * 100)
        
        return score, lst_skills
    
    def skills_match(self):
        
        # Load the skills data file
        skills = self.skills

        # Load data from ocr
        ocr_str, pages = self.ocr_text()
        ocr_ser = pd.Series(ocr_str)
        cleaned_words = hero.clean(ocr_ser)
        
        # Main dataframe for manipulation
        main_df = pd.DataFrame(cleaned_words[0].split(), columns = ['text'])
        
        # Details
        columns = ['filename', 'name', 'phone', 'email', 'companies',
                   'colleges', 'experience', 'skills',
                   'primary_score', 'primary_match',
                   'secondary_score', 'secondary_match',
                   'education_score', 'experience_score', 
                   'other_skills_match', 'document_similarity']
        details = pd.DataFrame(columns = columns)
        
        # Add the primary match and score
        pri_score, pri_match = find_match(main_df, skills[['Primary']])
        sec_score, sec_match = find_match(main_df, skills[['Secondary']])
        
        