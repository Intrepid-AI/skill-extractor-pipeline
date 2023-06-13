import spacy
import os 
from src.constants import Constants


from src.utilities import pdf_to_text,get_skills,unique_skills,make_directories, resume_jd_skills_matching, directory_structure, saving_pdf, path_for_saving_pdf
from src.preprocess import cleaning_text
from src.logger import get_logger
from src.db_ops import collection,update_db,add_db_request, add_db_request_jd_resume, update_db_jd_resume
from src.data_models import * 

make_directories([Constants.LOGS_FOLDER.value])
assert os.path.isdir(Constants.LOGS_FOLDER.value) == True  # Logs folder exists
LOGGER = get_logger(__name__)
LOGGER.info('Logs Folder Created')


LOGGER.info(f"DB initialised, collection: {collection} ready to use")

try:
    nlp = spacy.load(Constants.CORPUS.value)
    LOGGER.info("Corpus Loaded in Pipeline")
except Exception as e:
    LOGGER.error("Issue in Corpus loading- ", e)
skill_pattern_path = Constants.ANNOTATIONS.value

assert os.path.isfile(skill_pattern_path) == True  

ruler = nlp.add_pipe(Constants.ENTITY_RULER.value)

ruler.from_disk(skill_pattern_path)
LOGGER.info("Skills Annotations Loaded in Pipeline")

def skill_extractor(pdf_path):
  extracted_text = pdf_to_text(pdf_path)
  LOGGER.debug(f"Text extracted from resume {pdf_path}")
  cleaned_text = cleaning_text(extracted_text)
  skills = get_skills(cleaned_text,nlp)
  uniq_skills = unique_skills(skills)
  LOGGER.info(f"Extracted skills are {uniq_skills}")
  extracted_skills = {"SKILLS":uniq_skills}
  return extracted_skills


def skill_extractor2d(extracted_text):
  #extracted_text = pdf_to_text(pdf_path)
  cleaned_text = cleaning_text(extracted_text)
  skills = get_skills(cleaned_text,nlp)
  uniq_skills = unique_skills(skills)
  LOGGER.info(f"Extracted skills are {uniq_skills}")
  return uniq_skills


def pipe_line(file_name,file_path):
  uid = add_db_request(collection=collection,resume_name=file_name)
  LOGGER.info("Resume received validated, UUID Generated - {uid}".format(uid=uid))
  extracted_text = pdf_to_text(file_path)
  LOGGER.debug(f"Text extracted from resume {file_name}")
  cleaned_text = cleaning_text(extracted_text)
  skills = get_skills(cleaned_text,nlp)
  uniq_skills = unique_skills(skills)
  LOGGER.info(f"Extracted skills are {uniq_skills}")
  extracted_skills = {"SKILLS":uniq_skills}
  update_db(collection=collection,u_id=uid,resume_text=cleaned_text,skills=uniq_skills)
  return extracted_skills


def pipe_line_for_resume_jd_match(resume_file_name,resume_file_path,jd_file_name,jd_file_path):
  uid = add_db_request_jd_resume(collection=collection,resume_name=resume_file_name,jd_name=jd_file_name)
  LOGGER.info("Resume and Job Description received validated, UUID Generated - {uid}".format(uid=uid))
  resume_path,jd_path = directory_structure(uid=uid,type=Constants.RESUME_AND_JD.value)
  LOGGER.info("Directories for saving Resume and Job Description for UUID - {uid} created".format(uid=uid))
  extracted_text_resume = pdf_to_text(resume_file_path)
  LOGGER.debug(f"Text extracted from resume {resume_file_name}")

  resume_save_path = path_for_saving_pdf(parent_path=resume_path,pdf_name=resume_file_name)
  saving_pdf(pdf_object=resume_file_path,store_path=resume_save_path)
  LOGGER.debug(f"Resume saved at {resume_save_path}")

  extracted_text_jd = pdf_to_text(jd_file_path)
  LOGGER.debug(f"Text extracted from resume {jd_file_name}")

  jd_save_path = path_for_saving_pdf(parent_path=jd_path,pdf_name=jd_file_name)
  saving_pdf(pdf_object=jd_file_path,store_path=jd_save_path)
  LOGGER.debug(f"Job Description saved at {jd_save_path}")

  cleaned_text_resume = cleaning_text(extracted_text_resume)
  cleaned_text_jd = cleaning_text(extracted_text_jd)
  skills_resume = get_skills(cleaned_text_resume,nlp)
  skills_jd = get_skills(cleaned_text_jd,nlp)
  uniq_skills_resume = unique_skills(skills_resume)
  uniq_skills_jd = unique_skills(skills_jd)
  LOGGER.info(f"Extracted skills from resume are {uniq_skills_resume}")
  LOGGER.info(f"Skills required in Job Description resume are {uniq_skills_jd}")
  similiarity_percentage = resume_jd_skills_matching(unique_skills_resume=uniq_skills_resume,unique_skills_jd=uniq_skills_jd)
  LOGGER.info(f"Match Percentage is :{similiarity_percentage} to Requirement")
  extracted_skills = {"SKILLS":uniq_skills_resume, "required_skills":uniq_skills_jd, "Percentage":similiarity_percentage}
  update_db_jd_resume(collection=collection,u_id=uid,resume_text=cleaned_text_resume,jd_text=cleaned_text_jd,match=similiarity_percentage,skills=uniq_skills_resume,skills_jd=uniq_skills_jd)
  return extracted_skills

