# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:29:47 2021

@author: Dhaval
"""
import pytesseract
import os
import glob

from PIL import Image
from pdf2image import convert_from_path

# System path variables
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
poppler_path=r'C:\Users\MSI\Downloads\Release-21.03.0\poppler-21.03.0\Library\bin'

def ocr_text(filepath):
    
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
    
    return text_op, count


read_file = open('out_text.txt')
read_txt  = read_file.read()