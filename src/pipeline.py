import spacy
import os 
from src.constants import Constants


from src.utilities import pdf_to_text,get_skills,unique_skills,make_directories
from src.preprocess import cleaning_text
from src.logger import get_logger
from src.db_ops import collection,update_db,add_db_request
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


