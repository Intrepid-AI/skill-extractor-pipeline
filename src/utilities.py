import os
from typing import Any
import numpy as np
from datetime import datetime 
import filetype

import pdfplumber

from src.constants import Constants

from src.logger import get_logger

LOGGER = get_logger(__name__)


class Text_Extractor():
    '''This class will extract text from the pdf, doc, docx, txt, etc'''

    def __init__(self):
        pass

    def _find_file_type(self):
        pass
        '''
        Todo:
        '''
    def _extract_text_from_pdf_path(self):
        pass
        '''
        Todo:
        '''
    def _extract_text_from_pdf_bytes(self, byte_data):

        with pdfplumber.open(byte_data) as pdf:
            extracted_text = []
            
            for page in pdf.pages:
                text = page.extract_text()
                extracted_text.append(text)
            
            extracted_text = Constants.SPACE.value.join(extracted_text)
            
            return extracted_text
    
    def _extract_text_from_doc(self):
        pass
        '''
        Todo:
        '''
    def _extract_text_from_other(self):
        pass
        '''
        Todo:
        1. Support for copy paste in future
        2. Support for any other file type
        '''
        
    def extract_text(self, file, file_type=None):
        
        if file_type is None:
            pass
            '''
            Todo:
                1. Find the file type automatically
            '''            
        if file_type == Constants.ALLOWED_FILE_TYPES.value["pdf"]:
            return self._extract_text_from_pdf_bytes(file)
        
        elif file_type == Constants.ALLOWED_FILE_TYPES.value["doc"]:
            return self._extract_text_from_doc(file)

        else:
            LOGGER.error("File type not supported")
            raise Exception("File type not supported")
        
def unique_items(x):
    return list(set(x))

def make_directories(dir_list):
    for _dir_ in dir_list:
        if os.path.exists(_dir_):
            continue
        os.makedirs(_dir_)
        LOGGER.info("Directory {0} created".format(_dir_))

class Directory_Structure():
    '''This class will create the directory structure for the received data day wise'''

    date_today = None
    date_old = None
    todays_folder = None

    def __init__(self):
        pass

    def _isit_newday(self):
        '''This function will check if it is a new day or not'''
        today = datetime.now().date()
        
        if today != Directory_Structure.date_today:
        
            Directory_Structure.date_old = Directory_Structure.date_today
            Directory_Structure.date_today = today

            return True

        else:
        
            return False
        
    def _create_directory_for_newday(self):
        '''This function will create a directory for new day'''
        path = self._name_received_data_folder(Directory_Structure.date_today)
        make_directories([path])

        return path

    def _name_received_data_folder(self, dt):
        '''This function will name the folder for received data for passed date'''
        year,month,date = dt.strftime("%Y"), dt.strftime('%B_%Y'), dt.strftime('%d_%m_%Y')
        data = Constants.RECEIVED_DATA.value
        data_path = os.path.join(data,year,month,date)

        return data_path

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        '''This function will return the path for today's folder'''
        if self._isit_newday():
            LOGGER.info("New day detected")
            path = self._create_directory_for_newday()
            Directory_Structure.todays_folder = path
            return Directory_Structure.todays_folder

        else:

            return Directory_Structure.todays_folder

# import shutil
# from pathlib import Path
# from fastapi import UploadFile

def save_file(upload_file_byte, filepath : str):
    '''This function will save the file at the given path'''
    
    with open(filepath, "wb+") as buffer:
        buffer.write(upload_file_byte.read())
    
    # destination = Path(filepath)

    # try:
    #     with destination.open("wb+") as buffer:
    #         shutil.copyfileobj(upload_file.file, buffer)
    # finally:
    #     upload_file.file.close()

    LOGGER.debug("File saved at : {0}".format(filepath))

    return filepath

class Send_Response():
    '''This class is used to send the response back to the user'''
    
    def __init__(self, log_fn, db_fn):
        self.log_fn = log_fn
        self.db_fn = db_fn

    def update_response(self, db_client, resp_object, status, code=None, error=None):
        '''This function will update the status in db and response object and return it'''

        self.db_fn(db_client, status, resp_object.ID)
        
        resp_object.status = status
        resp_object.code = code if code else resp_object.code
        resp_object.error = error if error else resp_object.error

        return resp_object