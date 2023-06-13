import pdfplumber
from src.constants import Constants
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np
from datetime import datetime 
import shutil
import io


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

def resume_jd_skills_matching(unique_skills_resume,unique_skills_jd):
    # Train Word2Vec model on a corpus of skills
    corpus = [unique_skills_jd,unique_skills_resume] # Combine both lists into a corpus
    model = Word2Vec(corpus, min_count=1,)  # Train the Word2Vec model
    # Calculate average vector representations for each list of skills
    vector1 = np.mean([model.wv[skill] for skill in unique_skills_jd if skill in model.wv], axis=0)
    vector2 = np.mean([model.wv[skill] for skill in unique_skills_resume if skill in model.wv], axis=0)

    # Reshape the vectors if necessary
    vector1 = vector1.reshape(1, -1)  # Reshape to a row vector
    vector2 = vector2.reshape(1, -1)  # Reshape to a row vector

    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(vector1, vector2)
    match_percentage = similarity_matrix[0][0]*100
    return match_percentage


def directory_structure(uid,type):
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
 
