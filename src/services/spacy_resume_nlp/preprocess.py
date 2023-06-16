import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from src.constants import Constants

#To do: preload function for downloading and loading 
nltk.download([Constants.STOPWORDS.value,Constants.WORDNET.value])

def cleaning_text(text):
  review = re.sub(
        Constants.EXTRACT_STRUCTURE.value,
        Constants.SPACE.value,
        text,)
  review = review.lower()
  review = review.split()
  lm = WordNetLemmatizer()
  review = [
      lm.lemmatize(word)
      for word in review
      if not word in set(stopwords.words(Constants.LANGUAGE.value))
  ]
  review = Constants.SPACE.value.join(review)
  review = review.lower()
  cleaned_text = review
  return cleaned_text