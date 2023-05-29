import pdfplumber
from src.constants import Constants
import os

def pdf_to_text(pdf_path):
  with pdfplumber.open(pdf_path) as pdf:
      extracted_text = []
      for page in pdf.pages:
          text = page.extract_text()
          extracted_text.append(text)
      extracted_text = Constants.SPACE.value.join(extracted_text)
      return extracted_text


def get_skills(text,nlp):
    doc = nlp(text)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == Constants.SKILLS.value:
            subset.append(ent.text)
    myset.append(subset)
    return subset


def unique_skills(x):
    return list(set(x))

def make_directories(dir_list):
    for _dir_ in dir_list:
        if os.path.exists(_dir_):
            continue
        os.makedirs(_dir_)


def directory_structure():
    pass 
