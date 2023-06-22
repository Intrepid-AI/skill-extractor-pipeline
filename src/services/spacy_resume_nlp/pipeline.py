import os
import io

import spacy

from src.logger import get_logger

from src.constants import Constants

from src.data_models import *

from src.utilities import (pdf_to_text,unique_items,
                            make_directories, Directory_Structure, 
                            Text_Extractor)

from src.services.nlp_utilities import resume_jd_skills_matching

from src.services.spacy_resume_nlp.preprocess import cleaning_text

from src.db_ops import (add_task_info, update_db_jd_resume)

if os.path.isdir(Constants.LOGS_FOLDER.value) != True:
    make_directories([Constants.LOGS_FOLDER.value])

dir_manager = Directory_Structure()
text_extractor = Text_Extractor()

LOGGER = get_logger(__name__)

try: # Loading the corpus
    nlp_spacy = spacy.load(Constants.CORPUS.value)
    LOGGER.info("Corpus Loaded in Pipeline")
except Exception as e:
    LOGGER.error("Issue in Corpus loading- ", e)

skill_pattern_path = Constants.ANNOTATIONS.value
assert os.path.isfile(skill_pattern_path) == True  

ruler = nlp_spacy.add_pipe(Constants.ENTITY_RULER.value)
ruler.from_disk(skill_pattern_path)
LOGGER.info("Skills Annotations Loaded in Pipeline")

def get_skills(text,nlp_model):
    """_summary_"""
    doc = nlp_model(text)
    
    myset = []
    subset = []

    for ent in doc.ents:
        if ent.label_ == Constants.SKILLS.value:
            subset.append(ent.text)
    myset.append(subset)
    
    return subset

def skill_extractor(pdf_path, nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_"""

    extracted_text = pdf_to_text(pdf_path)
    LOGGER.debug(f"Text extracted from resume {pdf_path}")

    cleaned_text = cleaner_fn(extracted_text)

    skills = get_skills(cleaned_text,nlp_model)

    uniq_skills = unique_items(skills)
    LOGGER.info(f"Extracted skills are {uniq_skills}")

    extracted_skills = {"skilss":uniq_skills}

    return extracted_skills


def skill_extractor2d(extracted_text, nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_"""
    cleaned_text = cleaner_fn(extracted_text)
    
    skills = get_skills(cleaned_text,nlp_model)
    
    uniq_skills = unique_items(skills)
    LOGGER.info(f"Extracted skills are {uniq_skills}")
    
    return uniq_skills

'''
Todo:
1. Create a class which can be inherited by all the pipeline kind of functions which will have following methods:
'''

async def pipeline_skills_extraction(client, file, file_type, save_file_name, u_id,
                               nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_"""
    
    '''
    Todo : 
        1. Use pdf engine to extract text from pdf, it will also verify the mime type
        2. Exception handling of various failure points
        3. Format response with correct error codes
    '''
    file_name = os.path.basename(save_file_name)
    file_content = await file.read()
    file_object = io.BytesIO(file_content)

    extracted_text = text_extractor.extract_text(file_object, file_type)

    LOGGER.debug("Text extracted from resume {0}".format(file_name))
    
    cleaned_text = cleaner_fn(extracted_text)

    skills = get_skills(cleaned_text,nlp_model)
    
    uniq_skills = unique_items(skills)
    
    LOGGER.info("Extracted skills are {0}".format(uniq_skills))
    
    extracted_skills = {"skills":uniq_skills}
    
    add_task_info(client=client, u_id=u_id, resume_text=cleaned_text, skills=uniq_skills)
    
    return extracted_skills


async def pipeline_for_resume_jd_match(client, file_res, file_type_res, save_file_name_res,
                                    file_jd, file_type_jd, save_file_name_jd, u_id,
                                    nlp_model=nlp_spacy, cleaner_fn=cleaning_text):

    '''
    Todo : 
        1. Use pdf engine to extract text from pdf, it will also verify the mime type
        2. Exception handling of various failure points
        3. Format response with correct error codes
    '''

    file_name_res = os.path.basename(save_file_name_res)
    file_content_res = await file_res.read()
    file_object_res = io.BytesIO(file_content_res)
    extracted_text_resume = text_extractor.extract_text(file_object_res, file_type_res)
    LOGGER.debug("Text extracted from resume : {0}".format(file_name_res))

    file_name_jd = os.path.basename(save_file_name_jd)
    file_content_jd = await file_jd.read()
    file_object_jd = io.BytesIO(file_content_jd)
    extracted_text_jd = text_extractor.extract_text(file_object_jd, file_type_jd)
    LOGGER.debug("Text extracted from JD : {0}".format(file_name_jd))

    cleaned_text_resume = cleaning_text(extracted_text_resume)
    cleaned_text_jd = cleaning_text(extracted_text_jd)

    skills_resume = get_skills(cleaned_text_resume,nlp_spacy)
    skills_jd = get_skills(cleaned_text_jd,nlp_spacy)

    uniq_skills_resume = unique_items(skills_resume)
    uniq_skills_jd = unique_items(skills_jd)

    LOGGER.debug("Extracted skills from resume are {0}".format(uniq_skills_resume))
    LOGGER.debug("Skills required in Job Description resume are {0}".format(uniq_skills_jd))

    similiarity_percentage = resume_jd_skills_matching(unique_skills_resume=uniq_skills_resume,unique_skills_jd=uniq_skills_jd)
    LOGGER.info("Match Percentage is : {0} to Requirement".format(similiarity_percentage))
    
    extracted_skills = {"skills":uniq_skills_resume, "required_skills":uniq_skills_jd, "Percentage":similiarity_percentage}
    
    res_dict = {"u_id" : u_id, 
                "resume_text" : cleaned_text_resume, 
                "jd_text" : cleaned_text_jd, 
                "skills_res" : uniq_skills_resume, 
                "skills_jd" : uniq_skills_jd, 
                "match" : similiarity_percentage
                }
    '''
    Todo 1 :
        1. Correct the response and data models for response
    '''

    return extracted_skills

