# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 16:24:45 2021

@author: Dhaval
"""

import pandas as pd
import numpy as np
import pytesseract
import os
import glob
import texthero as hero

from pyresparser import ResumeParser
from pyresparser.utils import extract_text

from PIL import Image
from pdf2image import convert_from_path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class document_processing:
    
    def __init__(self, resume, skills, job_desc):
        
        skills = pd.read_csv('skills.csv')
        with open('Job_description.txt', 'rb') as file:
            job_desc = file.read()
        
        self.resume = resume
        self.skills = skills
        self.job_desc = job_desc
        
    def extract_resume(self):
        
        filepath = self.resume
        
        extension = filepath.split('.')[-1]
        extension = '.'+extension
        
        resume_ner = ResumeParser(filepath).get_extracted_data()
        resume_txt = extract_text(filepath, extension=extension)
        
        return resume_ner, resume_txt
        
    def ocr_text(self):
        
        filepath = self.resume
    
        files = glob.glob('temp/*')
        for f in files:
            os.remove(f)
        
        # Store all the pages of the PDF in a variable
        pages = convert_from_path(filepath, 500)
          
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
    
    def find_match(self, source, match):
        
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
    
    def fill_data(self, source, target, column):
        
        source.loc[0, column] = str(target[column])
        
        return source   
    
    def resume_cosine_score(self, text):
        
        jd_txt = self.job_desc
        jd_txt = pd.Series(jd_txt)
        jd_txt = hero.clean(jd_txt)
        jd_txt = jd_txt[0]
        
        text_list = [text, jd_txt]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_list)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 80
        match_percentage = round(match_percentage, 2)

        return match_percentage
        
    
    def skills_match(self):
        
        # Load the skills data file
        skills = self.skills
        
        # Load data from pyresparser
        pyres_data, pyres_text = self.extract_resume()
        self.data = pyres_data
        self.text = pyres_text
        
        # Load data from ocr
        #ocr_str, pages = self.ocr_text()
        ocr_ser = pd.Series(pyres_text)
        cleaned_words = hero.clean(ocr_ser)
        
        # Main dataframe for manipulation
        main_df = pd.DataFrame(cleaned_words[0].split(), columns = ['text'])
        self.clean_data = main_df
        
        # Num of words
        words = len(main_df)
        
        # Details
        columns = ['filename', 'name', 'mobile_number', 'email', 'company_names',
                   'college_name', 'experience', 'skills', 'experience_age',
                   'degree', 'words',
                   'primary_score', 'primary_match',
                   'secondary_score', 'secondary_match',
                   'no_of_pages', 'document_similarity']
        details = pd.DataFrame(columns = columns)
        
        # Add the primary match and score
        pri_score, pri_match = self.find_match(main_df, skills[['Primary']])
        sec_score, sec_match = self.find_match(main_df, skills[['Secondary']])
        
        # Add the document similarity score
        doc_sim = self.resume_cosine_score(cleaned_words[0])
        
        # Add details in a dataframe
        details.loc[0, 'filename'] = self.resume
        details = self.fill_data(details, pyres_data, 'name')
        details = self.fill_data(details, pyres_data, 'mobile_number')
        details = self.fill_data(details, pyres_data, 'email')
        details = self.fill_data(details, pyres_data, 'company_names')
        details = self.fill_data(details, pyres_data, 'college_name')
        details = self.fill_data(details, pyres_data, 'degree')
        details = self.fill_data(details, pyres_data, 'experience')
        details = self.fill_data(details, pyres_data, 'skills')
        details.loc[0, 'words'] = words
        
        if pyres_data['no_of_pages'] == None:
            details.loc[0, 'no_of_pages'] = 0
        else:
            details = self.fill_data(details, pyres_data, 'no_of_pages')
        details.loc[0, 'primary_score'] = pri_score
        details.loc[0, 'primary_match'] = str(pri_match)
        details.loc[0, 'secondary_score'] = sec_score
        details.loc[0, 'secondary_match'] = str(sec_match)
        details.loc[0, 'document_similarity'] = int(doc_sim)
        
        if pyres_data['total_experience'] > 0:
            details.loc[0, 'experience_age'] = pyres_data['total_experience']
        else:
            details.loc[0, 'experience_age'] = np.NaN
        
        details['no_of_pages'] = details['no_of_pages'].astype(int)
        
        return details
        
    