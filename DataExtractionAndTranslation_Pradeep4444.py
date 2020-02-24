#%%
# import PyPDF2
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from io import StringIO
from docx import Document
import re
import nltk
import pprint 
import spacy
import logging
import pdftotext
from pdf2image import convert_from_path

from googletrans import Translator

from pytesseract import image_to_string, image_to_pdf_or_hocr, image_to_data
from PIL import Image
import pytesseract
import os
import glob

import shutil
#%%
def google_trans(text_line):
    translator = Translator()
    result = translator.translate(text_line, dest = 'en')
    return (result.text)
#%%
## technique 2
# Iterate over all the pages
def arabic_to_english(input_file_location, input_file_name):
    file_location = os.path.join(input_file_location, input_file_name)
    ocr_page_nos = []
    pdftotext_file_location = os.path.join(input_file_location, 'pdftotext_op_pages_with_ocr')
    with open(file_location, "rb") as f:
        pdf = pdftotext.PDF(f)
    if not os.path.exists(pdftotext_file_location):
        os.mkdir(pdftotext_file_location)
    for count, page in enumerate(pdf):
        actual_count = count + 1
        text_content_location = f'{pdftotext_file_location}/pdftotext_pg_no_{actual_count}.txt'

        with open(text_content_location,'w') as t_handle:
            if (len(page) < 5):
                ocr_page_nos.append(actual_count)
                print(f'no text in page {actual_count}, possible ocr content')

            else:
                t_handle.write(page)
    print(ocr_page_nos)
    pages = convert_from_path(file_location, 500)

    for idx, i in enumerate(ocr_page_nos):

        tmp_image = pages[i]
        ocr_text = pytesseract.image_to_string(tmp_image,lang='ara')
        text_content_location = f'{pdftotext_file_location}/pdftotext_pg_no_{i}.txt'
        
        with open(text_content_location,'w') as t_handle:
            t_handle.write(ocr_text)
    #%%
    extracted_text_location = os.path.join(input_file_location,'extracted_pdf')
    if not os.path.exists(extracted_text_location):
        os.mkdir(extracted_text_location)
    tmp_extracted_file = os.path.join(extracted_text_location, 'extracted_text.txt')

    with open(tmp_extracted_file,'wb') as wfd:
        for i in range(1,len(pages)):
            text_content_location = f'{pdftotext_file_location}/pdftotext_pg_no_{i}.txt'
            with open(text_content_location,'rb') as fd:
                shutil.copyfileobj(fd, wfd)

    final_coverted_location = os.path.join(input_file_location, 'english_converted_files')
    if not os.path.exists(final_coverted_location):
        os.mkdir(final_coverted_location)
    converted_text_file_name = f'final_converted_{input_file_name}.txt'
    final_coverted_location = os.path.join(final_coverted_location, converted_text_file_name)

    with open(tmp_extracted_file,'r') as test_read:
        for idx, x in enumerate(test_read):
            # if idx == 10:
            #     break
            translated_text = google_trans(x)
            with open(final_coverted_location, 'a+') as w_handle:
                w_handle.write(translated_text)
                w_handle.write('\n')
    # clean up
    try:
        shutil.rmtree(extracted_text_location)
        print(f'deleted {extracted_text_location}')
        shutil.rmtree(pdftotext_file_location)
        print(f'deleted {pdftotext_file_location}')
    except:
        print('location not found')
#%%
# SET INPUT FILE LOCATIONS HERE
input_file_location = ''
if len(input_file_location) < 1:
    input_file_location = os.getcwd()
    test_file_name = 'arabic_test1.pdf'
files = os.listdir(input_file_location)
# arabic_to_english(input_file_location, test_file_name)
tmp = 0
for f in files:
    if f.endswith('.pdf'):
        tmp += 1
# tmp = len(files)
# print(tmp)

if tmp > 1:
    print('multiple files found')
    for idx, i in enumerate(files):
        tmp_file = os.path.join(input_file_location, i)
        arabic_to_english(input_file_location, i)
else:
    print('no files found, switching to local test file')
    try:
        arabic_to_english(input_file_location, 'arabic_test1.pdf')
    except:
        print('enter valid location')
