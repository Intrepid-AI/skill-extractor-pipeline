import os
import numpy as np
from datetime import datetime 

import pdfplumber

from src.constants import Constants

from src.logger import get_logger

LOGGER = get_logger(__name__)

def pdf_to_text(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
      extracted_text = []
      for page in pdf.pages:
          text = page.extract_text()
          extracted_text.append(text)
      extracted_text = Constants.SPACE.value.join(extracted_text)
      return extracted_text

def saving_pdf(pdf_object,store_path):
    bytes_content = pdf_object.getvalue()
    with open(store_path,"wb") as f:
        f.write(bytes_content)

def path_for_saving_pdf(parent_path,pdf_name):
    pdf_savepath = os.path.join(parent_path, pdf_name)
    return pdf_savepath

def unique_items(x):
    return list(set(x))

def make_directories(dir_list):
    for _dir_ in dir_list:
        if os.path.exists(_dir_):
            continue
        os.makedirs(_dir_)
        LOGGER.info("Directory {0} created".format(_dir_))

def directory_structure(uid,type):
    '''
    Todo:
        1. Separate create directory structure and file saving
    '''
    dt = datetime.now()
    month = dt.strftime('%B_%Y')
    date = dt.strftime('%d_%m_%Y')
    data = Constants.DATA.value
    processed_data = Constants.PROCESSED_DATA.value
    path = os.path.join(data,processed_data,month,date)
    uid_path = os.path.join(path,uid)
    resume_path = os.path.join(uid_path,Constants.RESUME.value)
    make_directories([resume_path])
    if type == Constants.RESUME_AND_JD.value:
        jd_path = os.path.join(uid_path,Constants.JD.value)
        make_directories([jd_path])
        return resume_path,jd_path
    
    return (resume_path)
 
