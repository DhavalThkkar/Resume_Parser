# -*- coding: utf-8 -*-
"""
Created on Sun Jul 11 12:33:48 2021

@author: Dhaval
"""

import pandas as pd
import os

from scripts.processing import document_processing
from tqdm import tqdm

import warnings
warnings.filterwarnings("ignore")

def document_score(df):
    
    # Page score
    df.loc[df['no_of_pages'] == 1, ['page_score']] = 100
    df.loc[df['no_of_pages'] == 2, ['page_score']] = 60
    df.loc[(df['no_of_pages'] > 2) |
           (df['no_of_pages'] == 0), ['page_score']] = 30
    
    # Word score
    df.loc[(df['words'] >= 200) & (df['words'] < 400),
           ['word_score']] = 100
    df.loc[(df['words'] >= 400) & (df['words'] < 600),
           ['word_score']] = 70
    df.loc[((df['words'] > 0) & (df['words'] < 200))|
           (df['words'] > 600) | (df['words'].isnull()),
           ['word_score']] = 40
    
    df['document_score'] = (df['page_score'] + df['word_score']) * 0.25
    
    df.drop(['word_score', 'page_score'], axis=1, inplace=True)
    
    return df

if __name__=='__main__':

    resume_dir = 'sample/'
    skills_file = 'skills.csv'
    jd_file = 'Job_description.txt'
    list_of_resumes = os.listdir(resume_dir)
    
    df = pd.DataFrame()
    for file in tqdm(list_of_resumes):
        result = document_processing(resume_dir+file, skills_file, jd_file)
        candidate = result.skills_match()
        df = pd.concat([df, candidate], ignore_index=True)
    
    df = document_score(df)
        
    # Final score
    df['Score'] = df['primary_score'] + df['secondary_score'] + df['document_score'] + df['document_similarity']
    
    # Sort by the score
    df = df.sort_values('Score', ascending=False)
    df = df.reset_index(drop=True)
    
    # Save the dataframe with the relevant details
    df.to_csv('Candidates_score.csv', index=False)