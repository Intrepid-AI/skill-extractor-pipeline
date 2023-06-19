import os

import spacy

from src.logger import get_logger

from src.constants import Constants

from src.data_models import *

from src.utilities import (pdf_to_text,unique_items,
                            make_directories, directory_structure, 
                            saving_pdf, path_for_saving_pdf)

from src.services.nlp_utilities import resume_jd_skills_matching

from src.services.spacy_resume_nlp.preprocess import cleaning_text

from src.db_ops import (collection,update_db,add_db_request, 
                        add_db_request_jd_resume, update_db_jd_resume)


make_directories([Constants.LOGS_FOLDER.value])
assert os.path.isdir(Constants.LOGS_FOLDER.value) == True  # Logs folder exists

LOGGER = get_logger(__name__)
LOGGER.info("Logs Folder Created")

LOGGER.info("DB initialised, collection: {0} ready to use".format(collection))

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
    """_summary_

    Args:
        text (_type_): _description_
        nlp_model (_type_): _description_

    Returns:
        _type_: _description_
    """
    doc = nlp_model(text)
    
    myset = []
    subset = []

    for ent in doc.ents:
        if ent.label_ == Constants.SKILLS.value:
            subset.append(ent.text)
    myset.append(subset)
    
    return subset

def skill_extractor(pdf_path, nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_

    Args:
        pdf_path (_type_): _description_
        nlp_model (_type_, optional): _description_. Defaults to nlp_spacy.
        cleaner_fn (_type_, optional): _description_. Defaults to cleaning_text.

    Returns:
        _type_: _description_
    """

    extracted_text = pdf_to_text(pdf_path)
    LOGGER.debug(f"Text extracted from resume {pdf_path}")

    cleaned_text = cleaner_fn(extracted_text)

    skills = get_skills(cleaned_text,nlp_model)

    uniq_skills = unique_items(skills)
    LOGGER.info(f"Extracted skills are {uniq_skills}")

    extracted_skills = {"skilss":uniq_skills}

    return extracted_skills


def skill_extractor2d(extracted_text, nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_

    Args:
        extracted_text (_type_): _description_
        cleaner_fn (_type_, optional): _description_. Defaults to cleaning_text.
        nlp_model (_type_, optional): _description_. Defaults to nlp_spacy.

    Returns:
        _type_: _description_
    """
    cleaned_text = cleaner_fn(extracted_text)
    
    skills = get_skills(cleaned_text,nlp_model)
    
    uniq_skills = unique_items(skills)
    LOGGER.info(f"Extracted skills are {uniq_skills}")
    
    return uniq_skills


def pipeline_skills_extraction(file_name,file_path, nlp_model=nlp_spacy, cleaner_fn=cleaning_text):
    """_summary_

    Args:
        file_name (_type_): _description_
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """

    uid = add_db_request(collection=collection,resume_name=file_name)
    LOGGER.info("Resume received validated, UUID Generated - {uid}".format(uid=uid))
    
    extracted_text = pdf_to_text(file_path)
    LOGGER.debug("Text extracted from resume {0}".format(file_name))
    
    cleaned_text = cleaner_fn(extracted_text)
    skills = get_skills(cleaned_text,nlp_model)
    uniq_skills = unique_items(skills)
    LOGGER.info("Extracted skills are {0}".format(uniq_skills))
    
    extracted_skills = {"skills":uniq_skills}
    
    update_db(collection=collection,u_id=uid,resume_text=cleaned_text,skills=uniq_skills)
    
    return extracted_skills


def pipeline_for_resume_jd_match(resume_file_name,resume_file_path,jd_file_name,jd_file_path):
    """_summary_

    Args:
        resume_file_name (_type_): _description_
        resume_file_path (_type_): _description_
        jd_file_name (_type_): _description_
        jd_file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    uid = add_db_request_jd_resume(collection=collection,
                                   resume_name=resume_file_name,jd_name=jd_file_name)
    LOGGER.info("Resume and Job Description received validated, UUID Generated - {uid}".format(uid=uid))
    
    resume_path,jd_path = directory_structure(uid=uid,type=Constants.RESUME_AND_JD.value)
    LOGGER.info("Directories for saving Resume and Job Description for UUID - {uid} created".format(uid=uid))
    
    extracted_text_resume = pdf_to_text(resume_file_path)
    LOGGER.debug("Text extracted from resume : {0}".format(resume_file_name))

    resume_save_path = path_for_saving_pdf(parent_path=resume_path,pdf_name=resume_file_name)
    saving_pdf(pdf_object=resume_file_path,store_path=resume_save_path)
    LOGGER.debug("Resume saved at : {0}".format(resume_save_path))

    extracted_text_jd = pdf_to_text(jd_file_path)
    LOGGER.debug("Text extracted from JD : {0}".format(jd_file_name))

    jd_save_path = path_for_saving_pdf(parent_path=jd_path,pdf_name=jd_file_name)
    saving_pdf(pdf_object=jd_file_path,store_path=jd_save_path)
    LOGGER.debug("Job Description saved at : {0}".format(jd_save_path))

    cleaned_text_resume = cleaning_text(extracted_text_resume)
    cleaned_text_jd = cleaning_text(extracted_text_jd)

    skills_resume = get_skills(cleaned_text_resume,nlp_spacy)
    skills_jd = get_skills(cleaned_text_jd,nlp_spacy)

    uniq_skills_resume = unique_items(skills_resume)
    uniq_skills_jd = unique_items(skills_jd)

    LOGGER.info("Extracted skills from resume are {0}".format(uniq_skills_resume))
    LOGGER.info("Skills required in Job Description resume are {0}".format(uniq_skills_jd))

    similiarity_percentage = resume_jd_skills_matching(unique_skills_resume=uniq_skills_resume,unique_skills_jd=uniq_skills_jd)
    LOGGER.info("Match Percentage is : {0} to Requirement".format(similiarity_percentage))
    
    extracted_skills = {"skills":uniq_skills_resume, "required_skills":uniq_skills_jd, "Percentage":similiarity_percentage}
    update_db_jd_resume(collection=collection,u_id=uid,resume_text=cleaned_text_resume,jd_text=cleaned_text_jd,match=similiarity_percentage,skills=uniq_skills_resume,skills_jd=uniq_skills_jd)

    return extracted_skills

