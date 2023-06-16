import streamlit as st
import pdfplumber
from src.services.spacy_resume_nlp.pipeline import skill_extractor_2
from src.logger import get_logger



LOGGER = get_logger(__name__)

uploaded_file = st.file_uploader('Upload Your Resume', type="pdf")
if uploaded_file is not None:
    LOGGER.info('Resume Uploaded')
    with pdfplumber.open(uploaded_file) as pdf:
        extracted_text = []
        for page in pdf.pages:
            text = page.extract_text()
            extracted_text.append(text)
        extracted_text = " ".join(extracted_text)
        LOGGER.info("Text extracted from Resume")

    a = st.button("Show Skills")
    if a:
        skills =skill_extractor_2(extracted_text)
        st.write(skills)

    

# from src.pipeline import skill_extractor

# if __name__ =="__main__":
#     skill_extractor('./artifacts/jc.pdf')